import functools
import asyncio


def coroutine(f):
    coroutine_f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coroutine_f(*args, **kwargs))
    return functools.update_wrapper(wrapper, coroutine_f)


def as_async(func):
    @functools.wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        partial_func = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, partial_func)
    return run
