from inspect import Parameter
from typing import Optional

from discord.ext import commands

from utils.context import ApolloContext
from utils.converters import AssetResponse, ImageConverter
from utils.image import wand_process

_old_transform = commands.Command.transform


def _transform(self, ctx, param):
	if param.annotation is Optional[ImageConverter]:
		if ctx.message.attachments:
			param = Parameter(
				param.name, param.kind, default=AssetResponse(ctx.message.attachments[0].url, 'image/gif'), annotation=ImageConverter)
		else:
			param = Parameter(
				param.name, param.kind, default=AssetResponse(ctx.author.avatar.url, 'image/gif'), annotation=ImageConverter)

	return _old_transform(self, ctx, param)


commands.Command.transform = _transform


class Image(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot
		self._cd_type = commands.BucketType.user
		self._cd = commands.CooldownMapping.from_cooldown(
			1, 30., self._cd_type)

	async def cog_check(self, ctx: ApolloContext):
		bucket = self._cd.get_bucket(ctx.message)
		retry_after = bucket.update_rate_limit()
		if retry_after:
			raise commands.CommandOnCooldown(
				self._cd, retry_after, self._cd_type)
		else:
			return True

	@commands.command(name='flip', descripton="Flip an image.", usage="[image]")
	async def _flip(self, ctx: ApolloContext, image: Optional[ImageConverter]):
		await wand_process(ctx, image, lambda frame: frame.flip())

	@commands.command(name='swirl', description="Swirl an image.", usage="[image]")
	async def _swirl(self, ctx: commands.Context, image: Optional[ImageConverter]):
		await wand_process(ctx, image, lambda frame: frame.swirl(degree=100))

	@commands.command(name='blur', description="Blur an image.", usage="[image]")
	async def _blur(self, ctx: commands.Context, image: Optional[ImageConverter]):
		await wand_process(ctx, image, lambda frame: frame.blur(sigma=20))

	@commands.command(name='sharpen', description="Sharpen an image.", usage="[image]")
	async def _sharpen(self, ctx: commands.Context, image: Optional[ImageConverter]):
		await wand_process(ctx, image, lambda frame: frame.sharpen(sigma=10))

	# @commands.command(name='eigishf', descripton="Eigishf meme.", usage="[image]")
	# async def _eigishf(self, ctx: ApolloContext, image: Optional[ImageConverter]):
	#     image = await url_to_bytes(ctx, image.url)
	#     image = PILImage.open(image).convert("RGBA")
	#     with PILImage.open('assets/eigishf.jpg') as final:
	#         image = image.resize((300, 300))
	#         final.paste(image, (250, 770), mask=image)
	#     image.close()
	#     await ctx.reply(file=file_from_bytes(ctx, final), can_delete=True)


def setup(bot) -> None:
	bot.add_cog(Image(bot))
