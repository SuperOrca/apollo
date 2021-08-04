import discord
from discord.ext import commands

import asyncio
import functools

__all__ = ("executor", "moderator", "administrator", "helper")


def executor(loop=None):
	loop = loop or asyncio.get_event_loop()

	def inner_function(func):
		@functools.wraps(func)
		def function(*args, **kwargs):
			partial = functools.partial(func, *args, **kwargs)
			return loop.run_in_executor(None, partial)

		return function

	return inner_function
