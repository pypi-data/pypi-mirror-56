import abc
from typing import Tuple


class Storage(abc.ABC):

    @abc.abstractmethod
    def increment(self, key: str) -> None:
        """Increment

            Should increment a value to
            keep track of how many errors
            occurs so the circuit breaker can open
        """
        pass

    @abc.abstractmethod
    def expire(self, key: str, ttl: int) -> None:
        """Expire

            Should set a time to live (ttl) on the key,
            the key should automatically vanish after the ttl defined
        """
        pass

    @abc.abstractmethod
    def get(self, key: str) -> int:
        """Get

            Should retrieve the value for the
            failure_key
        """
        pass


class BaseCircuitBreaker(abc.ABC):

    @abc.abstractmethod
    def storage(self) -> Storage:
        """Storage

            Should retrieve a instance of Storage
            that will be used to keep the circuit breaker
            status
        """
        pass

    @abc.abstractmethod
    def expected_exception(self) -> Tuple[Exception]:
        """Expected exceptions

            Should return a tuple of all exceptions
            that will be used to compute a fail
            and increment the circuit breaker
        """
        pass

    @abc.abstractmethod
    def failure_threshold(self) -> int:
        """Failure threshold
            The amount of failures required to open the circuit.
        """
        pass

    @abc.abstractmethod
    def recovery_timeout(self) -> int:
        """Recovery timeout

            Defines for how long the circuit key will remain in seconds,
            until it close the circuit again.
        """
        pass

    @abc.abstractmethod
    def failure_key(self) -> str:
        """Failure key

            Defines the key that will be used to store
            the circuit breaker errors counter.
        """
        pass

    def is_open(self) -> bool:
        """Is open

            Return rather the circuit is open or not
        """
        return self.storage.get(self.failure_key) >= self.failure_threshold

    def ping(self) -> None:
        """Ping

            Increment the failure key when some of
            the Exceptions defined on catch_exceptions occurs.
            Every time that the key is incremented the expire
            time will be renew
        """
        self.storage.increment(self.failure_key)
        self.storage.expire(self.failure_key, self.timeout)
