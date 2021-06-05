import pytest


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_need_to_fetch_only_upstream_commits():
    pass
