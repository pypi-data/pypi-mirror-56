import logging
import typing

logger = logging.Logger(__name__)


def basic_normalize(data: str) -> typing.Optional[str]:
    try:
        return data.lower().strip() or None
    except AttributeError:
        logger.error('invalid data in "to_lower" function "%s"' % data)
    return data


def remove_points(data: str) -> typing.Optional[str]:
    try:
        return data.replace('.', '') or None
    except AttributeError:
        logger.error('invalid data in "remove_points" function "%s"' % data)
    return data


def non_digit(data: str) -> typing.Optional[str]:
    try:
        return ''.join(i for i in data if not i.isdigit()) or None
    except AttributeError:
        logger.error('invalid data in "non_digit_before_dog" function "%s"' % data)
    return data


def only_digit(data: str) -> typing.Optional[str]:
    try:
        return ''.join(i for i in data if i.isdigit()) or None
    except AttributeError:
        logger.error('invalid data in "only_digit_before_dog" function "%s"' % data)
    return data


def str_unique_sorted_symbols(data: str) -> typing.Optional[str]:
    try:
        return ''.join(i for i in sorted(set(data))) or None
    except AttributeError:
        logger.error('invalid data in "str_to_sorted_set" function "%s"' % data)
    return data
