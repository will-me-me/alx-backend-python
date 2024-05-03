#!/usr/bin/env python3
"""Multiplier Module"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function"""
    def multiplier_function(x: float) -> float:
        return x * multiplier
    return multiplier_function
