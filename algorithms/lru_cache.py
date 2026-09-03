"""
Least Recently Used (LRU) Cache
O(1) time complexity for get and put operations.
"""
from typing import Any, Optional


class DNode:
    """Doubly linked list node for O(1) removal and insertion."""
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional['DNode'] = None
        self.next: Optional['DNode'] = None


class LRUCache:
    """
    LRU Cache implementation with fixed capacity.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache: dict[Any, DNode] = {}
        
        # Dummy head and tail nodes
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DNode) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: DNode) -> None:
        """Add node right after head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Optional[Any]:
        """Get the value for key, updating its recency."""
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update the value for key."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict least recently used (node before tail)
            lru_node = self.tail.prev
            if lru_node and lru_node != self.head:
                self._remove(lru_node)
                if lru_node.key in self.cache:
                    del self.cache[lru_node.key]

        new_node = DNode(key, value)
        self._add_to_front(new_node)
        self.cache[key] = new_node

    def __len__(self) -> int:
        return len(self.cache)
