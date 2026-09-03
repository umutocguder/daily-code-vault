"""Tests for Trie implementation."""
import unittest
try:
    from .trie import Trie
except ImportError:
    from trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        for word in ["apple", "app", "application", "apt", "banana", "band"]:
            self.trie.insert(word)

    def test_search(self):
        self.assertTrue(self.trie.search("app"))
        self.assertTrue(self.trie.search("apple"))
        self.assertFalse(self.trie.search("appl"))

    def test_starts_with(self):
        self.assertTrue(self.trie.starts_with("app"))
        self.assertTrue(self.trie.starts_with("ban"))
        self.assertFalse(self.trie.starts_with("cat"))

    def test_autocomplete(self):
        matches = self.trie.autocomplete("ap")
        self.assertEqual(matches, ["app", "apple", "application", "apt"])


if __name__ == "__main__":
    unittest.main()
