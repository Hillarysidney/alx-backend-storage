#!/usr/bin/env python3
"""Redis Module."""
import requests
import redis
from functools import wraps
from typing import Callable

cache = redis.Redis()


def store_cache(method: Callable) -> Callable:
    """Cache a value for 10 seconds."""
    @wraps(method)
    def wrapper(url):
        """The function wrapper."""
        if cache.get(url):
            return cache.get(url).decode()
        responses = method(url)
        cache.setex(url, 10, responses)
        return responses
    return wrapper


def track_url(method: Callable) -> Callable:
    """Cache a value for 10 seconds."""
    @wraps(method)
    def wrapper(url):
        """The function wrapper."""
        cache.incr(f'count:{url}')
        return method(url)
    return wrapper


@store_cache
@track_url
def get_page(url: str) -> str:
    """Get the responses of a webpage."""
    if cache.get(url):
        return cache.get(url).decode()
    responses = requests.get(url)
    return responses.text
