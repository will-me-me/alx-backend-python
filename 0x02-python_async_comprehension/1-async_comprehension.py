#!/usr/bin/env python3
""" Async Comprehension Module """
from typing import List

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """Returns 10 random numbders from"""
    return [num async for num in async_generator()]
