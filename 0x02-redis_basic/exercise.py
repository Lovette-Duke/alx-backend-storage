#!/usr/bin/env python3
'''script that uses the Redis NoSQL data storage to 
	write, read and update the db, also to store and retrive list
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''counts the number of times the Cache class is called.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''call the given method after incrementing counter.'''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''stores the history of inputs and outputs for the Cache class.'''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''returns output after storing history of inputs and outputs.'''
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    '''displays call history of Cache class' methods.'''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    func_name = fn.__qualname__
    input_key = '{}:inputs'.format(func_name)
    output_key = '{}:outputs'.format(func_name)
    func_call_count = 0
    if redis_store.exists(func_name) != 0:
        func_call_count = int(redis_store.get(func_name))
    print('{} was called {} times:'.format(func_name, func_call_count))
    func_inputs = redis_store.lrange(input_key, 0, -1)
    func_outputs = redis_store.lrange(output_key, 0, -1)
    for func_input, func_output in zip(func_inputs, func_outputs):
        print('{}(*{}) -> {}'.format(
            func_name,
            func_input.decode("utf-8"),
            func_output,
        ))


class Cache:
    '''an object that stores data in a Redis data storage.'''
    def __init__(self) -> None:
        '''initializes a cache class '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''method that stores values in a Redis data storage, returns the key.'''
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self,key: str,
            fn: Callable = None,) -> Union[str, bytes, int, float]:
        '''retrieves values from a Redis data storage.'''
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        '''retrieves a string from a Redis data storage.'''
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        '''retrieves an integer from a Redis data storage.'''
        return self.get(key, int)
