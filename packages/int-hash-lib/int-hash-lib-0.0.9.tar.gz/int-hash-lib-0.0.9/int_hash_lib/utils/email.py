import logging
import typing

from int_hash_lib import make_hs
from int_hash_lib.utils.normalizer import basic_normalize, remove_points, only_digit, str_unique_sorted_symbols, non_digit

logger = logging.getLogger(__name__)


def is_gmail(raw_data: str) -> bool:
    if not raw_data:
        return False
    elif 'gmail' in raw_data:
        return True
    return False


def email_valid_list(raw_data: str) -> typing.Tuple:
    if not raw_data:
        return tuple()
    left, right = list(filter(lambda x: x, raw_data.split('@')))
    return tuple((left, right))


def build_email_agg0(raw_data: str, salt) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = basic_normalize(raw_data)
        left, right = email_valid_list(data)
        if is_gmail(right):
            left = remove_points(left)
        data = '@'.join((left, right))
        result.update({'raw_data': raw_data, 'data': data, 'hs': make_hs(data, salt), 'error': None})
    except (ValueError, TypeError) as e:
        error = 'build_email_agg0 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def build_email_agg1(raw_data: str, salt) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        left, right = email_valid_list(raw_data)
        left = non_digit(left)
        hs = None if left is None else make_hs(left, salt)
        result.update({'raw_data': raw_data, 'data': left, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError) as e:
        error = 'build_email_agg1 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def build_email_agg2(raw_data: str, salt) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        left, right = list(filter(lambda x: x, raw_data.split('@')))
        left = only_digit(left)
        hs = None if left is None else make_hs(left, salt)
        result.update({'raw_data': raw_data, 'data': left, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError) as e:
        error = 'build_email_agg1 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def build_email_agg3(raw_data: str, salt) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = str_unique_sorted_symbols(raw_data)
        hs = None if data is None else make_hs(data, salt)
        result.update({'raw_data': raw_data, 'data': data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError) as e:
        error = 'build_email_agg1 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def collects_email_aggregates(raw_data: str, salt: str, **kwargs):
    agg0 = build_email_agg0(raw_data, salt)
    agg1 = build_email_agg1(agg0['data'], salt)
    agg2 = build_email_agg2(agg0['data'], salt)
    agg3 = build_email_agg3(agg1['data'], salt)
    return {
        'agg0': agg0['hs'],
        'agg1': agg1['hs'],
        'agg2': agg2['hs'],
        'agg3': agg3['hs'],
    }


__all__ = ['collects_email_aggregates']
