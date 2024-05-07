#!/usr/bin/env python3
""" Measure Runtime Module """
import asyncio
from time import perf_counter

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """Returns the total runtime for async_comprehension"""
    start = perf_counter()
    await asyncio.gather(*[async_comprehension() for _ in range(4)])
    return perf_counter() - start
