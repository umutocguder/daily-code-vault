"""
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
