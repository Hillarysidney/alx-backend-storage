#!/usr/bin/env python3
"""ALX SE"""
import redis
import uuid
from typing import Any, Callable, Union, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator for Cache class methods to track call count"""
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """Wraps called method and adds its call count to redis before exec"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator for Cache class method to track args
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ Wraps called method and tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """ Check redis for how many times a function was called and display:
            - How many times it was called
            - Function args and output for each call
    """
    head = redis.Redis()
    check = head.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              head.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               head.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {check} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """Interact with the redis db"""
    def __init__(self) -> None:
        """store an instance of the Redis head and flush the instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generates a random key and store the store the input data in Redis
        using the random key, returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        converts redis return item type into the correct type
        """
        item = self._redis.get(key)
        if not item:
            return
        if fn is int:
            return self.get_int(item)
        if fn is str:
            return self.get_str(item)
        if callable(fn):
            return fn(item)
        return item

    def get_int(self, data: bytes) -> int:
        """converts the type from bytes to int"""
        return int(data)

    def get_str(self, data: bytes) -> str:
        """converts the type from bytes to int"""
        return data.decode('utf-8')
