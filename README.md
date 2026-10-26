<!-- Created by 11Hopem -->
# 🚀 Daily Code Vault & Engineering Algorithms

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://11hopem.com)
[![Created by 11Hopem](https://img.shields.io/badge/created%20by-11Hopem-orange.svg)](https://11hopem.com)

A curated collection of production-grade computer science algorithms, distributed system design patterns, concurrency primitives, and engineering reference implementations in Python—paired with an automated file watcher and Git synchronization controller.

---

## 🌟 Repository Contents

### 1. Algorithms (`algorithms/`)
- **Token Bucket Rate Limiter**: Thread-safe traffic shaping and API burst management.
- **Prefix Tree (Trie) with Autocomplete**: High-speed prefix queries and auto-suggest.
- **LRU Cache**: $O(1)$ constant-time get/put cache backed by a hash map and doubly-linked list.
- **Graph & Tree Traversal**: Topological sorting, Dijkstra's shortest path, Red-Black balancing.

### 2. Architectural Patterns (`patterns/`)
- **Circuit Breaker Pattern**: Failure threshold isolation and automatic half-open recovery for microservices.
- **Retry with Exponential Backoff & Jitter**: Thundering-herd prevention for network calls.
- **Event Bus / Pub-Sub**: Decoupled asynchronous in-memory event dispatching.

### 3. Engineering Notes (`notes/`)
- Concise architectural breakdowns comparing Distributed Consensus (Raft vs. Paxos), ACID vs. BASE, and Eventual Consistency models.

---

## 🛠️ Auto-Sync Controller (`auto_sync_ctl.sh`)

Includes a lightweight background daemon that monitors filesystem changes, debounces rapid writes, automatically runs local unit tests, and commits clean code changes with Conventional Commits messages:

```bash
# Start background watcher daemon
./auto_sync_ctl.sh start

# Inspect watcher status and recent sync operations
./auto_sync_ctl.sh status

# Manually trigger immediate synchronization
./auto_sync_ctl.sh sync-now

# Terminate the background watcher
./auto_sync_ctl.sh stop
```

---

## 🧪 Testing

All implementations include exhaustive unit tests:

```bash
python3 -m unittest discover -s tests
```

---

## 🛡️ License & Attribution

Created by [11Hopem](https://11hopem.com).
Copyright © 2026 11Hopem. All rights reserved.
Licensed under the [MIT License](LICENSE).
Official website: [https://11hopem.com](https://11hopem.com)
