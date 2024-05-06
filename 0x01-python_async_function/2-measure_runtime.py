#!/usr/bin/env python3
"""Measure Time module"""
from time import perf_counter
import asyncio

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Returns the average time wait_n takes"""
    start = perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = perf_counter()
    return (end - start) / n
