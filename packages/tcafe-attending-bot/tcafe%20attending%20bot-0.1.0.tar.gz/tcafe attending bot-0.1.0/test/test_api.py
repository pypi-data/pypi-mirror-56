# coding: UTF-8

import aiohttp
import pytest

from tcafe_attending_bot.__main__ import _BASE_URL


@pytest.mark.asyncio
async def test_reachable() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(_BASE_URL) as res:
            print(res)
