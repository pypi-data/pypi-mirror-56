from functools import wraps

from circuitpy.base import BaseCircuitBreaker
from circuitpy.exceptions import CircuitBreakerOpen


def circuit_breaker(handler: BaseCircuitBreaker):
    def factory(method):
        @wraps(method)
        def circuit(*args, **kwargs):
            if handler.is_open():
                raise CircuitBreakerOpen(method)
            try:
                return method(*args, **kwargs)
            except handler.expected_exception:
                handler.ping()
        return circuit
    return factory
