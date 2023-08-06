import logging
import typing

from app.hasher import make_hs

logger = logging.Logger(__name__)


def build_ua_agg0(raw_data: str, salt: str) -> typing.Dict:
    result = {'raw_data': raw_data, 'data': None, 'hs': None, 'error': None}
    try:
        data = raw_data.split('[')[0]
        hs = make_hs(data, salt)
        result.update({'raw_data': raw_data, 'data': data, 'hs': hs, 'error': None})
    except (AttributeError, ValueError, TypeError, IndexError) as e:
        error = 'build_ua_agg0 error for value: %s, error: %s' % (raw_data, e)
        logger.error(error)
        result.update({'error': error})
    return result


def collect_user_agent_aggregates(raw_data: str, salt: str, **kwargs) -> typing.Dict:
    agg0 = build_ua_agg0(raw_data, salt)
    return {
        'agg0': agg0['hs'],
    }


__all__ = ['collect_user_agent_aggregates']
