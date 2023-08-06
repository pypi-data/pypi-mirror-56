import csv
import datetime
import hashlib
import importlib
import logging
import typing
from io import StringIO

logger = logging.getLogger(__name__)


def make_hs(s: str, salt: str) -> int:
    try:
        if s is None:
            return
        separator = b':'
        bs = bytes(s, encoding='utf-8')
        b_salt = bytes(salt, encoding='utf-8')
        data = bs + separator + b_salt
        hs = int(hashlib.sha256(data).hexdigest(), 32)
        return int(str(hs)[10:28])
    except Exception as e:
        logger.error('make_hash error : %s' % e)


def prepare_hash_by_key(k: str, v: typing.Any, salt: str, region: str, mapping: typing.Dict) -> typing.Dict:
    mod = importlib.import_module('app.utils')
    func_name = mapping.get(k, None)
    hs_func = getattr(mod, func_name) if func_name else None
    if hs_func is None or v is None or v == '':
        return
    if isinstance(v, (typing.List, typing.Tuple)):
        v = [hs_func(str(i), salt=salt, region=region) for i in v]
    else:
        v = hs_func(str(v), salt=salt, region=region)
    return v


def make_hash_from_dict(data: typing.Dict, salt: str, region: str,
                        first_only_keys: (typing.List, typing.Tuple), mapping: typing.Dict) -> typing.Dict:
    item = {}

    def get_first(data):
        if isinstance(data, typing.Dict):
            return {'agg0': data.get('agg0')}
        if isinstance(data, (typing.List, typing.Tuple)):
            data = [{'agg0': d.get('agg0')} for d in data]
        return data

    def one_or_many(item):
        if len(item.values()) == 1:
            return list(item.values())[0]
        return item

    for k, v in data.items():
        hs = prepare_hash_by_key(k, v, salt=salt, region=region, mapping=mapping)
        logger.debug('key: %s, value: %s, hs_result: %s', (k, v, hs))
        if hs:
            if k in first_only_keys:
                hs = get_first(hs)
            if isinstance(hs, (typing.List, typing.Tuple)):
                val = ','.join([str(one_or_many(d)) for d in hs])
                item[k] = val
            else:  # here is dict
                val = one_or_many(hs)
                if isinstance(val, typing.Dict):
                    for ik, iv in val.items():
                        item['%s_%s' % (k, ik)] = iv
                else:
                    item[k] = val
        else:
            if isinstance(v, (datetime.datetime, datetime.date)):
                v = str(v)
            item[k] = v
    return item


def make_hash_from_csv(in_file, salt: str, region: str, schema, first_only_keys: (typing.List, typing.Tuple),
                       mapping: typing.Dict):
    try:
        in_file = in_file.decode('utf-8').splitlines()
    except AttributeError:
        pass
    rd = csv.reader(in_file, delimiter=',', quotechar='"')
    headers = next(rd, None)
    with StringIO() as f:
        for idx, row in enumerate(rd):
            row = [str(r).strip() if len(r.split(',')) < 2 else list(filter(None, r.split(','))) for r in row]
            row_dict = dict(zip(headers, row))
            invalid_fields = schema().validate(data=row_dict).keys()
            for i in invalid_fields:
                row_dict[i] = None
            row_dict = schema().load(data=row_dict, unknown='EXCLUDE')
            # logger.info('before: %s' % {k: str(v) for k, v in row_dict.items()})
            data = make_hash_from_dict(data=row_dict, salt=salt, region=region, first_only_keys=first_only_keys,
                                       mapping=mapping)
            # logger.info('after: %s' % data)
            if idx == 0:
                csv.writer(f).writerow(list(data.keys()))
            csv.writer(f).writerow(list(data.values()))
        return f.getvalue()
