import logging
import typing

import phonenumbers
from app.hasher import make_hs

logger = logging.Logger(__name__)


def build_phone_agg0(raw_data: str, region: str, salt: str) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = phonenumbers.parse(raw_data, region=region)
        if sum((phonenumbers.is_valid_number(data), phonenumbers.is_possible_number(data),
                region == phonenumbers.region_code_for_number(data))) != 3:
            error = 'data: %s, error: invalid phone number' % raw_data
            logger.error(error)
            result.update({'error': error})
            return result
        result.update({'data': str(data.national_number), 'hs': make_hs(str(data.national_number), salt)})
    except phonenumbers.phonenumberutil.NumberParseException as e:
        error = 'data: %s, error: %s' % (raw_data, e)
        result.update({'error': error})
        logger.error(error)
    return result


def build_phone_agg_remove_last_symbol(raw_data: str, salt, symbols_count: int) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = raw_data[:-symbols_count]
        hs = make_hs(data, salt)
        result.update({'raw_data': raw_data, 'data': data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError, IndexError) as e:
        error = 'build_phone_agg_remove_last_symbol error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def collect_phone_aggregates(raw_data: str, salt: str, region: str, **kwargs) -> typing.Dict:
    agg0 = build_phone_agg0(raw_data, region, salt)
    agg1 = build_phone_agg_remove_last_symbol(agg0['data'], salt, 1)
    agg2 = build_phone_agg_remove_last_symbol(agg0['data'], salt, 2)
    agg3 = build_phone_agg_remove_last_symbol(agg0['data'], salt, 3)
    agg4 = build_phone_agg_remove_last_symbol(agg0['data'], salt, 4)
    return {
        'agg0': agg0['hs'],
        'agg1': agg1['hs'],
        'agg2': agg2['hs'],
        'agg3': agg3['hs'],
        'agg4': agg4['hs'],
    }


__all__ = ['collect_phone_aggregates']
