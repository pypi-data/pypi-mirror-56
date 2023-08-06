import functools
import logging
import queue
import threading

__all__ = ['threaded']

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
