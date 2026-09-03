"""
Prefix Tree (Trie) with Autocomplete support.
"""
from typing import Dict, List, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    """
    Standard Trie with search, prefix matching, and word retrieval.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns True if the word is in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the trie that starts with prefix."""
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str, max_results: int = 5) -> List[str]:
        """Finds all words starting with the given prefix up to max_results."""
        node = self._find_node(prefix)
        if not node:
            return []

        results: List[str] = []
        self._dfs(node, prefix, results, max_results)
        return results

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node: TrieNode, path: str, results: List[str], limit: int) -> None:
        if len(results) >= limit:
            return
        if node.is_end_of_word:
            results.append(path)
        for char, child_node in sorted(node.children.items()):
            if len(results) >= limit:
                break
            self._dfs(child_node, path + char, results, limit)
