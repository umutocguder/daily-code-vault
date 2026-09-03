"""Tests for Circuit Breaker Pattern."""
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
