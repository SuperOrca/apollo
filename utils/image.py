from io import BytesIO
from typing import Any
from utils.converters import AssetResponse

import discord
from wand.image import Image
from asyncdagpi import ImageFeatures
from discord.ext import commands

from utils.context import ApolloContext


async def dagpi_process(ctx: ApolloContext, image: Any, feature: str, **kwargs) -> None:
	"""A method that uses dagpi to process images."""
	image = to_asset(image)
	image = await ctx.bot.dagpi.image_process(getattr(ImageFeatures, feature)(), url=image.url, **kwargs)
	file = discord.File(image.image, f'render.{image.format}')
	await ctx.reply(file=file, can_delete=True)


async def url_to_bytes(ctx, url) -> BytesIO:
	"""A method that fetches bytes from a url."""
	response = await ctx.bot.session.get(url)
	buffer = await response.read()
	if buffer.__sizeof__() > 10 * (2 ** 20):
		raise commands.UserInputError("Exceeded 10MB.")
	blob = BytesIO(buffer)
	blob.seek(0)
	return blob


def to_asset(image: Any) -> AssetResponse:
	if isinstance(image, AssetResponse):
		return image
	else:
		return AssetResponse(str(image), 'image/gif')


async def wand_process(ctx: ApolloContext, image: Any, operation) -> None:
	image = to_asset(image)
	blob = await url_to_bytes(ctx, image.url)
	if image.is_animated():
		_format = 'gif'
		with Image(blob=blob) as new:
			for i, frame in enumerate(new.sequence):
				operation(frame)
				new.sequence[i] = frame
			buffer = new.make_blob(format=_format)
	else:
		_format = 'png'
		with Image(blob=blob) as new:
			operation(new)
			buffer = new.make_blob(format=_format)
	await ctx.reply(file=discord.File(BytesIO(buffer), f'render.{_format}'), can_delete=True)
