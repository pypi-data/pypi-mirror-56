import ipaddress
import logging
import typing

from int_hash_lib import make_hs

logger = logging.Logger(__name__)


def build_ip_agg0(raw_data: str, salt: str) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = str(ipaddress.IPv4Address(raw_data))
        hs = make_hs(data, salt)
        result.update({'raw_data': raw_data, 'data': data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError, IndexError) as e:
        error = 'build_ip_agg0 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def build_ip_agg1(raw_data: str, salt: str) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = '.'.join(raw_data.split('.')[:-1])
        hs = make_hs(data, salt)
        result.update({'raw_data': raw_data, 'data': data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError, IndexError) as e:
        error = 'build_ip_agg1 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def collect_ip_address_aggregates(raw_data: str, salt: str, **kwargs) -> typing.Dict:
    agg0 = build_ip_agg0(raw_data, salt)
    agg1 = build_ip_agg1(agg0['data'], salt)
    return {
        'agg0': agg0['hs'],
        'agg1': agg1['hs']
    }


__all__ = ['collect_ip_address_aggregates']
