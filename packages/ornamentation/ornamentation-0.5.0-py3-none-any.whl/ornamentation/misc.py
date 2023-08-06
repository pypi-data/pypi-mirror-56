import functools
import logging
import os
import queue
import threading

from decorator import decorator

__all__ = ['skip', 'skip_if_env', 'threaded']

logger = logging.getLogger(__name__)


def threaded(function, daemon=False):
    """Decorator adapted from http://stackoverflow.com/a/14331755/18992 (thanks bj0)."""

    def wrapped_function(q, *args, **kwargs):
        rtn = function(*args, **kwargs)
        q.put(rtn)

    @functools.wraps(function)
    def worker(*args, **kwargs):
        q = queue.Queue()

        t = threading.Thread(
            target=wrapped_function, args=(q,) + args, kwargs=kwargs
        )
        t.daemon = daemon
        t.start()
        t.result = q
        return t

    return worker


def skip(function):
    @functools.wraps(function)
    def wrapped_function(*args, **kwargs):
        return None

    return wrapped_function


@decorator
def skip_if_env(function, envar='SKIP', *args, **kwargs):
    if os.environ.get(envar, ''):
        return None
    return function(*args, **kwargs)
