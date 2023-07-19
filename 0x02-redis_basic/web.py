#!/usr/bin/env python3
"""
Implements an expiring web cache and tracker.

- The code defines a decorator that counts how many times a URL is accessed.
- It uses Redis as a cache to store and retrieve web pages.
- The cached values expire after a certain time period.
- The `get_page` function fetches a web page and caches its value using the decorator.
"""

from typing import Callable
from functools import wraps
import redis
import requests

redis_client = redis.Redis()


def url_count(method: Callable) -> Callable:
    """Decorator that counts how many times a URL is accessed"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")  # Increment the count for the URL
        cached = redis_client.get(f'{url}')  # Check if the URL is already cached
        if cached:
            return cached.decode('utf-8')  # Return the cached value

        # Cache the value for the URL and set an expiration time of 10 seconds
        redis_client.setex(f'{url}', 10, method(url))

        return method(*args, **kwargs)  # Call the original method

    return wrapper


@url_count
def get_page(url: str) -> str:
    """Fetch a web page and cache its value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

