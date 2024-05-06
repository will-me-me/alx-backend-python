#!/usr/bin/env python3
"""Wait N module"""
import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Returns list of all delays"""
    tasks = [asyncio.create_task(wait_random(max_delay)) for i in range(n)]
    await_times = await asyncio.gather(*tasks, return_exceptions=False)
    return sorted(await_times)
