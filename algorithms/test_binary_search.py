"""Tests for Binary Search."""
import unittest
from .binary_search import binary_search


class TestBinarySearch(unittest.TestCase):
    def test_found(self):
        arr = [1, 3, 5, 7, 9, 11]
        self.assertEqual(binary_search(arr, 5), 2)
        self.assertEqual(binary_search(arr, 1), 0)
        self.assertEqual(binary_search(arr, 11), 5)

    def test_not_found(self):
        arr = [1, 3, 5, 7, 9, 11]
        self.assertIsNone(binary_search(arr, 6))
        self.assertIsNone(binary_search(arr, 0))


if __name__ == "__main__":
    unittest.main()
