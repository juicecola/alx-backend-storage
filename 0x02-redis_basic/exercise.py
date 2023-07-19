#!/usr/bin/env python3
"""
Cache Class:

- The Cache class uses Redis as a data store.
- It provides methods to store and retrieve data in Redis.
- It also includes decorators to count method calls and store the history of inputs and outputs.
"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs of a method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for the decorated method"""
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data

    return wrapper


def replay(fn: Callable):
    """Display the history of calls for a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        try:
            input_data = input_data.decode("utf-8")
        except Exception:
            input_data = ""

        try:
            output_data = output_data.decode("utf-8")
        except Exception:
            output_data = ""

        print("{}(*{}) -> {}".format(function_name, input_data, output_data))


class Cache:
    """Cache class that uses Redis as a data store"""

    def __init__(self):
        """Initialize the Cache class with a Redis client instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a randomly generated key"""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis using a given key and optionally apply a conversion function"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve data from Redis as a string"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Retrieve data from Redis as an integer"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value

