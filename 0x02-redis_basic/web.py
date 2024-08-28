#!/usr/bin/env python3
''' script scrapes, stores and retrives HTML content'''


import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def cache_data(method: Callable) -> Callable:
    '''caches the output of scraped data.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''wrappers function for caching the output.'''
        redis_store.incr(f'count:{url}')
        res = redis_store.get(f'result:{url}')
        if res:
            return res.decode('utf-8')
        res = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, res)
        return res
    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''returns the content of a URL, caches the request's response,
    and tracks the request.'''
    return requests.get(url).text
