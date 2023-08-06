import logging
import time
import warnings

from decorator import decorator

__all__ = ['debug', 'deprecated', 'timeit']

logger = logging.getLogger(__name__)


@decorator
def timeit(function, report_func=print, *args, **kwargs):
    """Prints the call and how long it took."""
    ts = time.time()
    try:
        result = function(*args, **kwargs)
    except Exception as e:
        raise e
    finally:
        te = time.time()
        msg = f'{function.__name__}({args}, {kwargs}) took {te - ts:.2} sec'
        report_func(msg)
    return result


@decorator
def debug(function, report_func=print, *args, **kwargs):
    """Emits debugging message when function is called."""
    function = timeit(function, report_func=report_func)
    try:
        result = function(*args, **kwargs)
    except Exception as e:
        msg = f'{function.__name__}({args}, {kwargs}) errored {type(e).__name__} - {e}'
        raise e
    else:
        msg = f'{function.__name__}({args}, {kwargs}) returned {result}'
    finally:
        report_func(msg)

    return result


@decorator
def deprecated(function, *args, **kwargs):
    """Mark a function as deprecated. Will emit a deprecation warning."""
    warnings.warn(
        f'Call to deprecated function: {function.__name__}',
        category=DeprecationWarning,
    )
    return function(*args, **kwargs)
