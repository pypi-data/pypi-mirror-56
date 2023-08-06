from inspect import signature
from datetime import datetime


class CircuitBreakerOpen(Exception):

    def __init__(self, method):
        self.method = method

    def __str__(self):
        full_date = datetime.today().strftime("%D %H:%M:%S")
        return "[{full_date}] - circuit breaker is open " \
                "for method \"{name}\" ".format(
                    full_date=full_date,
                    name=self.method.__name__
                )
