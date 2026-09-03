"""
Binary Search and Lower/Upper Bound utilities.
"""
from typing import Sequence, Any, Optional


def binary_search(array: Sequence[Any], target: Any) -> Optional[int]:
    """Finds index of target in a sorted sequence, or None if not found."""
    low, high = 0, len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None
