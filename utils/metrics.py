import datetime
import time
from typing import Any, Union

import discord
from discord.colour import Colour
from discord.embeds import MaybeEmpty, _EmptyEmbed
from discord.types.embed import EmbedType


def isImage(url):
	"""A method that checks if a url is an image."""
	url = url.lower()
	return bool(
		url.endswith("png")
		or url.endswith("jpg")
		or url.endswith("jpeg")
		or url.endswith("webp")
	)

class Embed(discord.Embed):
	def __init__(self, *, colour: Union[int, Colour, _EmptyEmbed], color: Union[int, Colour, _EmptyEmbed], title: MaybeEmpty[Any], type: EmbedType, url: MaybeEmpty[Any], description: MaybeEmpty[Any], timestamp: datetime.datetime):
		self.color = 0x515b72
		super().__init__(colour=colour, color=color, title=title, type=type, url=url, description=description, timestamp=timestamp)


class Timer:
	def __init__(self):
		self._start = None
		self._end = None

	def start(self):
		self._start = time.perf_counter()

	def stop(self):
		self._end = time.perf_counter()

	def __enter__(self):
		self.start()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.stop()

	def __int__(self):
		return round(self.time)

	def __float__(self):
		return self.time

	def __str__(self):
		return str(self.time)

	def __repr__(self):
		return f"<Timer time={self.time}>"

	@property
	def time(self):
		if self._end is None:
			raise ValueError("Timer has not been ended.")
		return self._end - self._start
