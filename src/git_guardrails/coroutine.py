import functools
import asyncio


def coroutine(f):
    async def ff():
        await f()

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ff(*args, **kwargs))
    return functools.update_wrapper(wrapper, ff)
