import functools
import asyncio


def coroutine(f):
    coroutine_f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coroutine_f(*args, **kwargs))
    return functools.update_wrapper(wrapper, coroutine_f)
