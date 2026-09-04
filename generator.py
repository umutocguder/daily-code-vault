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

# Additional Rich Catalogue Modules
ADDITIONAL_MODULES = [
    {
        "category": "algorithms",
        "name": "min_heap",
        "title": "Min Heap & Priority Queue",
        "description": "Binary min-heap supporting push, pop-min, and O(N) heapify with strict type invariants.",
        "code": '''"""
Min Heap (Priority Queue) Implementation
O(log N) push and pop, O(1) peek.
"""
from typing import List, Any, Optional


class MinHeap:
    def __init__(self, elements: Optional[List[Any]] = None):
        self._heap: List[Any] = []
        if elements:
            self._heap = list(elements)
            self._build_heap()

    def _build_heap(self) -> None:
        """Transforms list into heap in O(N) time."""
        for i in reversed(range(len(self._heap) // 2)):
            self._sift_down(i)

    def push(self, item: Any) -> None:
        """Adds an item into the heap."""
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> Any:
        """Removes and returns the minimum element."""
        if not self._heap:
            raise IndexError("pop from empty heap")
        min_item = self._heap[0]
        last_item = self._heap.pop()
        if self._heap:
            self._heap[0] = last_item
            self._sift_down(0)
        return min_item

    def peek(self) -> Optional[Any]:
        """Returns the minimum element without removing it."""
        return self._heap[0] if self._heap else None

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self._heap[idx] < self._heap[parent]:
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        size = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest == idx:
                break
            self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
            idx = smallest

    def __len__(self) -> int:
        return len(self._heap)
''',
        "test": '''"""Tests for MinHeap."""
import unittest
try:
    from .min_heap import MinHeap
except ImportError:
    from min_heap import MinHeap


class TestMinHeap(unittest.TestCase):
    def test_push_and_pop(self):
        heap = MinHeap()
        for num in [7, 3, 10, 1, 5]:
            heap.push(num)
        self.assertEqual([heap.pop() for _ in range(5)], [1, 3, 5, 7, 10])

    def test_build_heap(self):
        heap = MinHeap([15, 2, 8, 1, 9])
        self.assertEqual(heap.peek(), 1)
        self.assertEqual(heap.pop(), 1)
        self.assertEqual(heap.pop(), 2)

    def test_empty_heap_exception(self):
        heap = MinHeap()
        with self.assertRaises(IndexError):
            heap.pop()


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "algorithms",
        "name": "consistent_hashing",
        "title": "Consistent Hashing Ring",
        "description": "Consistent Hash Ring with virtual nodes for minimal remapping during node changes.",
        "code": '''"""
Consistent Hashing Ring with Virtual Nodes
"""
import hashlib
import bisect
from typing import Dict, List, Optional


class ConsistentHashRing:
    def __init__(self, replicas: int = 100):
        self.replicas = replicas
        self.ring: List[int] = []
        self.node_map: Dict[int, str] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        """Adds a server node with multiple virtual replicas on the ring."""
        for i in range(self.replicas):
            v_key = f"{node}#replica_{i}"
            h = self._hash(v_key)
            idx = bisect.bisect_left(self.ring, h)
            self.ring.insert(idx, h)
            self.node_map[h] = node

    def remove_node(self, node: str) -> None:
        """Removes a server node and all its virtual replicas."""
        for i in range(self.replicas):
            v_key = f"{node}#replica_{i}"
            h = self._hash(v_key)
            idx = bisect.bisect_left(self.ring, h)
            if idx < len(self.ring) and self.ring[idx] == h:
                del self.ring[idx]
            self.node_map.pop(h, None)

    def get_node(self, key: str) -> Optional[str]:
        """Finds the server node assigned to the key."""
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.node_map[self.ring[idx]]
''',
        "test": '''"""Tests for ConsistentHashRing."""
import unittest
try:
    from .consistent_hashing import ConsistentHashRing
except ImportError:
    from consistent_hashing import ConsistentHashRing


class TestConsistentHashRing(unittest.TestCase):
    def test_routing(self):
        ring = ConsistentHashRing(replicas=50)
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")

        node_a = ring.get_node("user_1001")
        node_b = ring.get_node("user_1002")
        self.assertIn(node_a, ["node1", "node2", "node3"])
        self.assertIn(node_b, ["node1", "node2", "node3"])

    def test_remove_node(self):
        ring = ConsistentHashRing(replicas=30)
        ring.add_node("node1")
        self.assertEqual(ring.get_node("session_key"), "node1")
        ring.remove_node("node1")
        self.assertIsNone(ring.get_node("session_key"))


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "patterns",
        "name": "observer_bus",
        "title": "Decoupled Event Observer Bus",
        "description": "Thread-safe event publishing and subscription system supporting multiple topics and typed payloads.",
        "code": '''"""
Event Bus / Observer Pattern
"""
import threading
from collections import defaultdict
from typing import Callable, Dict, List, Any


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)
        self._lock = threading.Lock()

    def subscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        """Register a subscriber handler for a specific topic."""
        with self._lock:
            self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        """Unregister an existing subscriber."""
        with self._lock:
            if handler in self._subscribers[topic]:
                self._subscribers[topic].remove(handler)

    def publish(self, topic: str, payload: Any = None) -> int:
        """Broadcasts payload to all handlers subscribed to the topic."""
        with self._lock:
            handlers = list(self._subscribers.get(topic, []))

        for h in handlers:
            h(payload)
        return len(handlers)
''',
        "test": '''"""Tests for EventBus."""
import unittest
try:
    from .observer_bus import EventBus
except ImportError:
    from observer_bus import EventBus


class TestEventBus(unittest.TestCase):
    def test_publish_subscribe(self):
        bus = EventBus()
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe("order_created", handler)
        count = bus.publish("order_created", {"id": 42})

        self.assertEqual(count, 1)
        self.assertEqual(received, [{"id": 42}])

    def test_unsubscribe(self):
        bus = EventBus()
        received = []
        handler = lambda x: received.append(x)
        bus.subscribe("tick", handler)
        bus.unsubscribe("tick", handler)
        bus.publish("tick", "payload")
        self.assertEqual(received, [])


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "algorithms",
        "name": "topological_sort",
        "title": "Topological Sort (Kahn's Algorithm)",
        "description": "Detects dependency order in Directed Acyclic Graphs (DAGs) and identifies dependency cycles.",
        "code": '''"""
Topological Sort using Kahn's Algorithm (In-degree traversal).
"""
from collections import deque, defaultdict
from typing import Dict, List, Set, Optional


class DependencyGraph:
    def __init__(self):
        self.adj: Dict[str, List[str]] = defaultdict(list)
        self.nodes: Set[str] = set()

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Directed edge: from_node must run before to_node."""
        self.adj[from_node].append(to_node)
        self.nodes.add(from_node)
        self.nodes.add(to_node)

    def sort(self) -> Optional[List[str]]:
        """Returns valid linear ordering, or None if cyclic."""
        in_degree = {node: 0 for node in self.nodes}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1

        queue = deque([node for node, deg in in_degree.items() if deg == 0])
        ordered: List[str] = []

        while queue:
            node = queue.popleft()
            ordered.append(node)
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return ordered if len(ordered) == len(self.nodes) else None
''',
        "test": '''"""Tests for Topological Sort."""
import unittest
try:
    from .topological_sort import DependencyGraph
except ImportError:
    from topological_sort import DependencyGraph


class TestTopologicalSort(unittest.TestCase):
    def test_valid_dag(self):
        g = DependencyGraph()
        g.add_edge("build", "test")
        g.add_edge("test", "deploy")
        order = g.sort()
        self.assertIsNotNone(order)
        self.assertTrue(order.index("build") < order.index("test") < order.index("deploy"))

    def test_cycle_detection(self):
        g = DependencyGraph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "A")
        self.assertIsNone(g.sort())


if __name__ == "__main__":
    unittest.main()
'''
    },
    {
        "category": "patterns",
        "name": "retry_with_backoff",
        "title": "Exponential Backoff & Jitter",
        "description": "Production retry mechanism with full jitter to avoid the thundering herd problem.",
        "code": '''"""
Exponential Backoff with Full Jitter
"""
import random
import time
from typing import Callable, Any, Type, Tuple


def retry_with_backoff(
    func: Callable[..., Any],
    max_retries: int = 3,
    base_delay: float = 0.05,
    max_delay: float = 1.0,
    retry_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    sleep_fn: Callable[[float], None] = time.sleep
) -> Any:
    """Retries a callable using exponential backoff with full jitter."""
    attempt = 0
    while True:
        try:
            return func()
        except retry_exceptions as err:
            attempt += 1
            if attempt > max_retries:
                raise err
            # Exponential delay with full jitter
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jittered_delay = random.uniform(0, delay)
            sleep_fn(jittered_delay)
''',
        "test": '''"""Tests for Retry with Backoff."""
import unittest
try:
    from .retry_with_backoff import retry_with_backoff
except ImportError:
    from retry_with_backoff import retry_with_backoff


class TestRetry(unittest.TestCase):
    def test_eventual_success(self):
        attempts = 0
        def unstable():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise ConnectionError("Temporary outage")
            return "OK"

        result = retry_with_backoff(unstable, max_retries=3, sleep_fn=lambda _: None)
        self.assertEqual(result, "OK")
        self.assertEqual(attempts, 3)

    def test_exceeded_retries(self):
        def always_fail():
            raise ValueError("Fatal error")

        with self.assertRaises(ValueError):
            retry_with_backoff(always_fail, max_retries=2, sleep_fn=lambda _: None)


if __name__ == "__main__":
    unittest.main()
'''
    }
]

MODULES.extend(ADDITIONAL_MODULES)
