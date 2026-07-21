import time
from functools import wraps


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=3,
        recovery_timeout=10
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None


    def call(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":

                if (
                    time.time() - self.last_failure_time
                    < self.recovery_timeout
                ):
                    raise Exception(
                        "Circuit breaker is open"
                    )

                self.state = "HALF_OPEN"
            try:
                result = await func(*args, **kwargs)
                self.failures = 0
                self.state = "CLOSED"

                return result


            except Exception:
                self.failures += 1
                self.last_failure_time = time.time()

                if self.failures >= self.failure_threshold:
                    self.state = "OPEN"
                raise

        return wrapper