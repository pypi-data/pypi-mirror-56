from functools import wraps
import time
from contextlib import contextmanager
import types


def process_duration(duration):
    if duration < 1:
        took = f"{duration *1000:.2f} msec"
    elif duration < 60:
        took = f"{duration:.4f} sec"
    else:
        m = duration // 60
        sec = duration % 60
        took = f"{m} min {sec} sec"
    return took


def timer(func):
    'Print a duration of a function execution'

    start = time.time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            duration = end - start

            print(f'Function: {func.__name__} took {process_duration(duration)}')

    return wrapper


@contextmanager
def time_codeblock():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f'Block of code took: {process_duration(end-start)}')


class multimethod:
    def __init__(self, func):
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults + 1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self


if __name__ == '__main__':
    class Spam:
        @multimethod
        def hello(self, *args):
            # Default method called if no match
            raise TypeError('No matching method for hello')

        @hello.match(int, int)
        def hello(self, x, y):
            print(x, y)

        @hello.match(str)
        def hello(self, name):
            print(name)
