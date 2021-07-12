from functools import wraps, partial

from discord.ext import commands
import asyncio

def typing(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        executed: Optional[Any] = None

        for obj in set(args):
            if isinstance(obj, commands.Context):
                async with obj.typing():
                    executed = await func(*args, **kwargs)
                break
            else:
                continue

        return executed

    return wrapper

def asyncexe():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            partial = partial(func, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(None, partial)

        return wrapper

    return decorator
