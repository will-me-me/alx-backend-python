#!/usr/bin/env python3
"""Element length Module"""

from typing import Sequence, Tuple, List, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return list of tuple of sequence and integer."""
    return [(i, len(i)) for i in lst]
