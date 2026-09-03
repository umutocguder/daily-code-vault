"""Tests for LRU Cache."""
import unittest
try:
    from .lru_cache import LRUCache
except ImportError:
    from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_basic_put_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)

    def test_eviction(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Evicts 'a'
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_update_recency_on_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # 'a' is now most recently used
        cache.put("c", 3)  # Evicts 'b'
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("c"), 3)


if __name__ == "__main__":
    unittest.main()
