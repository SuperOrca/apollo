import asyncio
from functools import wraps


def asyncexe():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            partial = partial(func, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(None, partial)

        return wrapper

    return decorator
