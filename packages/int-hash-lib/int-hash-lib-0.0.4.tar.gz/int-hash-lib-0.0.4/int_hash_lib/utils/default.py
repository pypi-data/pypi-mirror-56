import logging
import typing

from app.hasher import make_hs

logger = logging.Logger(__name__)


def build_agg0(raw_data: str, salt: str) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        hs = None if raw_data is None else make_hs(raw_data, salt)
        result.update({'raw_data': raw_data, 'data': raw_data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError) as e:
        error = 'build_agg0 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def collect_hash_aggregates(raw_data: str, salt: str, **kwargs) -> typing.Dict:
    agg0 = build_agg0(raw_data, salt)
    return {
        'agg0': agg0['hs'],
    }


__all__ = ['collect_hash_aggregates']
