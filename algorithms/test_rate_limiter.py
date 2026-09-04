"""Tests for Token Bucket Rate Limiter."""
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
