#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from functools import lru_cache, wraps


with open(os.path.join(os.path.dirname(__file__), 'version.txt')) as file:
    __version__ = file.read().strip()
__package__ = 'incolumepy.singleton_decorator'


@lru_cache()
def singleton(cls):
    ''' Decorator for classes '''
    instances = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper
