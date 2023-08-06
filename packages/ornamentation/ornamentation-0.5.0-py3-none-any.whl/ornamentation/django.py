import functools
import logging

__all__ = ['admin_action']

logger = logging.getLogger(__name__)


def admin_action(function):
    """Decorator to turn method into admin actions."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    wrapper.short_description = wrapper.__doc__
    return wrapper
