from io import BytesIO
from typing import Union
from time import time

import discord
from discord.ext import commands
from wand.image import Image as WandImage
from PIL import Image as PILImage

from utils.context import ApolloContext
from utils.image import imageToBytes, fileFromBytes, getImage, create_minecraft_blocks, process_minecraft


class Image(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        if not hasattr(bot, "minecraft_blocks"):
            self.bot.minecraft_blocks = {}
            self.bot.loop.create_task(create_minecraft_blocks(self.bot))
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(1, 7., self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='flip', descripton="Flip an image.", usage="flip [image]")
    async def _flip(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with PILImage.open(blob) as image:
            new_image = image.rotate(180)
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='wide', descripton="Widen an image.", usage="wide [image]")
    async def _wide(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with await PILImage.open(blob) as image:
            new_image = image.resize((image.height * 2, image.width))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")

    @commands.command(name='ultrawide', descripton="Ultra widen an image.", usage="ultrawide [image]")
    async def _ultrawide(self, ctx: ApolloContext,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with PILImage.open(blob) as image:
            new_image = image.resize((image.height * 4, image.width))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='squish', descripton="Squish an image.", usage="squish [image]")
    async def _squish(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with PILImage.open(blob) as image:
            new_image = image.resize((image.height, image.width * 2))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='ultrasquish', descripton="Ultrasquish an image.", usage="ultrasquish [image]")
    async def _ultrasquish(self, ctx: ApolloContext,
                           image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with PILImage.open(blob) as image:
            new_image = image.resize((image.height, image.width * 4))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='swirl', description="Swirl an image.", usage="swirl [image]")
    async def _swirl(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        blob = await imageToBytes(ctx, image)
        with WandImage(blob=blob) as image:
            image.swirl(degree=100)
            buffer = image.make_blob('png')
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {(end-start) * 1000:,.0f}ms")
        await ctx.reply(file=fileFromBytes(ctx, BytesIO(buffer)), embed=embed, can_delete=True)

    @commands.command(name='minecraft', description="Get image as minecraft blocks.", usage="minecraft [image]",
                      aliases=['mc'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _minecraft(self, ctx: ApolloContext, image: Union[
            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        """
        Credits to The Anime Bot (https://github.com/Cryptex-github/the-anime-bot-bot) (ver cool dude)
        """
        b = await imageToBytes(ctx, image)
        start = time()
        file = discord.File(await process_minecraft(self.bot, b), f"{ctx.command.name}.png")
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(
            text=f"Processed in {(end-start) * 1000:,.0f}ms | Credits to The Anime Bot")
        await ctx.send(file=file,
                       embed=embed, can_delete=True)


def setup(bot) -> None:
    bot.add_cog(Image(bot))
