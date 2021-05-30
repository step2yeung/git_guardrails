import asyncio
import pytest
from git_guardrails.coroutine import as_async, coroutine


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_as_async_decorator():
    @as_async
    def f():
        return 42

    f_result = await f()
    assert f_result == 42


def test_coroutine_decorator():
    @coroutine
    def f():
        yield from asyncio.sleep(1)
        return 42

    f_result = f()
    assert f_result == 42
