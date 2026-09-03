"""
Daily Code & Journal Generator
Generates clean, well-tested algorithms, design patterns, and tech notes.
"""

import os
import sys
import random
from datetime import datetime

MODULES = [
    {
        "category": "algorithms",
        "name": "lru_cache",
        "title": "Least Recently Used (LRU) Cache",
        "description": "An efficient LRU Cache using a doubly linked list and hash map for O(1) get and put operations.",
        "code": '''"""
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
''',
        "test": '''"""Tests for LRU Cache."""
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
        cache.put("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_update_recency_on_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("c"), 3)


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "patterns",
        "name": "circuit_breaker",
        "title": "Circuit Breaker Pattern",
        "description": "Prevents cascading service failures in distributed systems.",
        "code": '''"""
Circuit Breaker Pattern
States: CLOSED (normal), OPEN (failing), HALF-OPEN (recovery check).
"""
import time
from enum import Enum
from typing import Callable, Any, Optional


class State(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected by open circuit."""
    pass


class CircuitBreaker:
    """
    Manages failure tracking and recovery transitions.
    """
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 5.0,
        half_open_success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_success_threshold = half_open_success_threshold

        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes the wrapped function under circuit breaker protection."""
        current_time = time.time()

        if self.state == State.OPEN:
            if self.last_failure_time and (current_time - self.last_failure_time >= self.recovery_timeout):
                self.state = State.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN. Fast failing request.")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self) -> None:
        if self.state == State.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_success_threshold:
                self.state = State.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == State.CLOSED:
            self.failure_count = 0

    def _on_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.state in (State.CLOSED, State.HALF_OPEN) and self.failure_count >= self.failure_threshold:
            self.state = State.OPEN
''',
        "test": '''"""Tests for Circuit Breaker Pattern."""
import unittest
import time
try:
    from .circuit_breaker import CircuitBreaker, CircuitBreakerOpenException, State
except ImportError:
    from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException, State


class TestCircuitBreaker(unittest.TestCase):
    def test_closed_state_success(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        res = cb.call(lambda x: x * 2, 5)
        self.assertEqual(res, 10)
        self.assertEqual(cb.state, State.CLOSED)

    def test_trip_to_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        def failing():
            raise ValueError("API error")

        for _ in range(2):
            with self.assertRaises(ValueError):
                cb.call(failing)

        self.assertEqual(cb.state, State.OPEN)
        with self.assertRaises(CircuitBreakerOpenException):
            cb.call(lambda: 42)


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "algorithms",
        "name": "trie",
        "title": "Prefix Tree (Trie) with Autocomplete",
        "description": "Fast prefix search tree supporting word insertion, prefix checking, and autocomplete queries.",
        "code": '''"""
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
''',
        "test": '''"""Tests for Trie implementation."""
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
'''
    },
    {
        "category": "algorithms",
        "name": "rate_limiter",
        "title": "Token Bucket Rate Limiter",
        "description": "Production-grade token bucket rate limiter for API traffic shaping and concurrency control.",
        "code": '''"""
Token Bucket Rate Limiter
Allows bursts while maintaining a consistent average rate.
"""
import time
import threading
from typing import Optional


class TokenBucketRateLimiter:
    """
    Thread-safe Token Bucket Rate Limiter.
    """
    def __init__(self, capacity: float, refill_rate: float):
        """
        :param capacity: Max burst capacity in tokens
        :param refill_rate: Tokens added per second
        """
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def allow_request(self, tokens_needed: float = 1.0) -> bool:
        """Checks and consumes tokens if available."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False
''',
        "test": '''"""Tests for Token Bucket Rate Limiter."""
import unittest
import time
try:
    from .rate_limiter import TokenBucketRateLimiter
except ImportError:
    from rate_limiter import TokenBucketRateLimiter


class TestTokenBucket(unittest.TestCase):
    def test_burst_within_capacity(self):
        limiter = TokenBucketRateLimiter(capacity=3, refill_rate=1)
        self.assertTrue(limiter.allow_request(1))
        self.assertTrue(limiter.allow_request(1))
        self.assertTrue(limiter.allow_request(1))
        self.assertFalse(limiter.allow_request(1))


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "notes",
        "name": "distributed_consensus_notes",
        "title": "Distributed Consensus & Raft Protocol",
        "description": "Concise architectural breakdown of Raft Consensus vs Paxos.",
        "code": '''"""
Architectural Notes: Raft vs Paxos Consensus
"""

CONSENSUS_PRINCIPLES = {
    "Leader Election": "Heartbeats trigger randomized timeouts to elect a unique leader.",
    "Log Replication": "Leader accepts client commands, appends to log, and broadcasts AppendEntries RPCs.",
    "Safety Guarantee": "Election safety, Leader Append-Only, and Log Matching Invariants ensure linearizability.",
}


def get_consensus_summary() -> dict:
    return CONSENSUS_PRINCIPLES
''',
        "test": '''"""Tests for distributed consensus notes."""
import unittest
try:
    from .distributed_consensus_notes import get_consensus_summary
except ImportError:
    from distributed_consensus_notes import get_consensus_summary


class TestNotes(unittest.TestCase):
    def test_summary_keys(self):
        summary = get_consensus_summary()
        self.assertIn("Leader Election", summary)
        self.assertIn("Log Replication", summary)


if __name__ == "__main__":
    unittest.main()
'''
    }
]


def generate_entry(output_base_dir: str = ".") -> dict:
    """Selects an unwritten module or creates a new entry and updates the journal."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure directories exist with __init__.py
    categories = ["algorithms", "patterns", "notes"]
    for cat in categories:
        cat_path = os.path.join(output_base_dir, cat)
        os.makedirs(cat_path, exist_ok=True)
        init_file = os.path.join(cat_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write('"""Module package initialization."""\n')

    # Check which modules are not yet written
    chosen = None
    for module in MODULES:
        target_path = os.path.join(output_base_dir, module["category"], f"{module['name']}.py")
        if not os.path.exists(target_path):
            chosen = module
            chosen_name = module['name']
            break
            
    if not chosen:
        chosen = random.choice(MODULES)
        chosen_name = f"{chosen['name']}_{today_str.replace('-', '_')}"

    cat_dir = os.path.join(output_base_dir, chosen["category"])
    code_path = os.path.join(cat_dir, f"{chosen_name}.py")
    test_path = os.path.join(cat_dir, f"test_{chosen_name}.py")

    # Write code
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(chosen["code"])

    # Write test
    test_content = chosen["test"].replace(f".{chosen['name']}", f".{chosen_name}").replace(f"import {chosen['name']}", f"import {chosen_name}")
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_content)

    # Update index log
    log_entry = f"- **{today_str}** `[{chosen['category'].upper()}]` **{chosen['title']}** - {chosen['description']} (`{chosen['category']}/{chosen_name}.py`)\n"
    journal_path = os.path.join(output_base_dir, "JOURNAL.md")
    
    existing_content = ""
    if os.path.exists(journal_path):
        with open(journal_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
    else:
        existing_content = "# Daily Code & Engineering Vault\n\nAutomated daily repository tracking algorithms, software patterns, and technical notes.\n\n## Activity Log\n\n"

    with open(journal_path, "w", encoding="utf-8") as f:
        if "## Activity Log\n\n" in existing_content:
            parts = existing_content.split("## Activity Log\n\n", 1)
            f.write(parts[0] + "## Activity Log\n\n" + log_entry + parts[1])
        else:
            f.write(existing_content + "\n" + log_entry)

    commit_message = f"feat({chosen['category']}): add {chosen['title']} [{today_str}]"
    
    # Write commit message for workflow consumption
    with open(os.path.join(output_base_dir, ".last_commit_msg"), "w", encoding="utf-8") as f:
        f.write(commit_message)

    return {
        "title": chosen["title"],
        "category": chosen["category"],
        "code_path": code_path,
        "test_path": test_path,
        "commit_message": commit_message
    }


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result = generate_entry(base_dir)
    print(f"Generated: {result['title']}")
    print(f"Commit message: {result['commit_message']}")
