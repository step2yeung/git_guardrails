from functools import wraps
from asyncio import run


def coroutine(f):
    """
    Wraps a function in `asyncio.run`
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return run(f(*args, **kwargs))

    return wrapper
