from functools import wraps

from discord.ext import commands


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
