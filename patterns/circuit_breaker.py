"""
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
