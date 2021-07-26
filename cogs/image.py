from io import BytesIO
from typing import Optional

import discord
from PIL import Image as PILImage
from discord.ext import commands
from inspect import Parameter
from wand.image import Image as WandImage

from utils.context import ApolloContext
from utils.image import fileFromBytes, create_minecraft_blocks, process_minecraft
from utils.converters import ImageConverter

_old_transform = commands.Command.transform


def _transform(self, ctx, param):

    if param.annotation is Optional[ImageConverter]:
        loop = ctx.bot.loop

        if ctx.message.attachments:
            param = Parameter(
                param.name, param.kind, default=loop.create_task(ImageConverter().convert(ctx.message.attachments[0].url)), annotation=ImageConverter)
        else:
            param = Parameter(
                param.name, param.kind, default=loop.create_task(ImageConverter().convert(ctx.author.avatar.url)), annotation=ImageConverter)

    return _old_transform(self, ctx, param)


commands.Command.transform = _transform


class Image(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        if not hasattr(bot, "minecraft_blocks"):
            self.bot.minecraft_blocks = {}
            self.bot.loop.create_task(create_minecraft_blocks(self.bot))
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 10., self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(
                self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='flip', descripton="Flip an image.", usage="flip [image]")
    async def _flip(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        with PILImage.open(image) as image:
            new_image = image.rotate(180)
        await ctx.reply(file=fileFromBytes(ctx, new_image), can_delete=True)

    @commands.command(name='wide', descripton="Widen an image.", usage="wide [image]")
    async def _wide(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        with PILImage.open(image) as image:
            new_image = image.resize((image.height * 2, image.width))
        await ctx.reply(file=fileFromBytes(ctx, new_image), can_delete=True)

    @commands.command(name='ultrawide', descripton="Ultra widen an image.", usage="ultrawide [image]")
    async def _ultrawide(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        with PILImage.open(image) as image:
            new_image = image.resize((image.height * 4, image.width))
        await ctx.reply(file=fileFromBytes(ctx, new_image), can_delete=True)

    @commands.command(name='squish', descripton="Squish an image.", usage="squish [image]")
    async def _squish(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        with PILImage.open(image) as image:
            new_image = image.resize((image.height, image.width * 2))
        await ctx.reply(file=fileFromBytes(ctx, new_image), can_delete=True)

    @commands.command(name='ultrasquish', descripton="Ultrasquish an image.", usage="ultrasquish [image]")
    async def _ultrasquish(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        with PILImage.open(image) as image:
            new_image = image.resize((image.height, image.width * 4))
        await ctx.reply(file=fileFromBytes(ctx, new_image), can_delete=True)

    @commands.command(name='swirl', description="Swirl an image.", usage="swirl [image]")
    async def _swirl(self, ctx: commands.Context, image: Optional[ImageConverter]):
        with WandImage(blob=image) as image:
            image.swirl(degree=100)
            buffer = image.make_blob('png')
        file = discord.File(BytesIO(buffer), f'{ctx.command.name}.png')
        await ctx.reply(file=file, can_delete=True)

    @commands.command(name='blur', description="Blur an image.", usage="blur [image]")
    async def _blur(self, ctx: commands.Context, image: Optional[ImageConverter]):
        with WandImage(blob=image) as image:
            image.blur(sigma=20)
            buffer = image.make_blob('png')
        file = discord.File(BytesIO(buffer), f'{ctx.command.name}.png')
        await ctx.reply(file=file, can_delete=True)

    @commands.command(name='sharpen', description="Sharpen an image.", usage="sharpen [image]")
    async def _sharpen(self, ctx: commands.Context, image: Optional[ImageConverter]):
        with WandImage(blob=image) as image:
            image.sharpen(sigma=10)
            buffer = image.make_blob('png')
        file = discord.File(BytesIO(buffer), f'{ctx.command.name}.png')
        await ctx.reply(file=file, can_delete=True)

    @commands.command(name='eigishf', descripton="Eigishf meme.", usage="eigishf [image]")
    async def _eigishf(self, ctx: ApolloContext, image: Optional[ImageConverter]):
        image = PILImage.open(image)
        with PILImage.open('assets/eigishf.jpg') as final:
            image = image.resize((300, 300))
            final.paste(image, (250, 770), image)
        image.close()
        await ctx.reply(file=fileFromBytes(ctx, final), can_delete=True)

    @commands.command(name='minecraft', description="Get image as minecraft blocks.", usage="minecraft [image]",
                      aliases=['mc'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _minecraft(self, ctx: ApolloContext, image: Optional[ImageConverter], quality: int = 64) -> None:
        """
        Credits to The Anime Bot (https://github.com/Cryptex-github/the-anime-bot-bot) (ver cool dude)
        """
        if 128 < quality or quality < 1:
            raise commands.BadArgument("Quality must be between 1 and 128.")
        file = discord.File(await process_minecraft(self.bot, image, quality), f"{ctx.command.name}.png")
        await ctx.reply(file=file, can_delete=True)


def setup(bot) -> None:
    bot.add_cog(Image(bot))
