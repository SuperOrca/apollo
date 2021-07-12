from os import getenv
from typing import Union
from io import BytesIO

import asyncdagpi
import discord
from discord.ext import commands

from utils.image import dagpi_process, imageToPIL, fileFromBytes
from utils.wrappers import typing


class Image(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='pixelate', description="Shows the image as pixelated.", usage="pixelate [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _pixelate(self, ctx: commands.Context,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.pixel())

    @commands.command(name='colors', description="Shows the image's colors.", usage="colors [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _colors(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.colors())

    @commands.command(name='america', description="Shows the image as america.", usage="america [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _america(self, ctx: commands.Context,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.america(), end="gif")

    @commands.command(name='communism', description="Shows the image as communism.", usage="communism [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _communism(self, ctx: commands.Context,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.communism(), end="gif")

    @commands.command(name='triggered', description="Shows the image as triggered.", usage="triggered [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _triggered(self, ctx: commands.Context,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.triggered(), end="gif")

    @commands.command(name='wasted', description="Shows the image as wasted.", usage="wasted [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wasted(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.wasted())

    @commands.command(name='invert', description="Shows the image as inverted.", usage="invert [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _invert(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.invert())

    @commands.command(name='sobel', description="Shows the image as sobel.", usage="sobel [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sobel(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.sobel())

    @commands.command(name='hog', description="Shows the image as a hog.", usage="hog [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _hog(self, ctx: commands.Context,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.hog())

    @commands.command(name='triangle', description="Shows the image as a triangle.", usage="triangle [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _triangle(self, ctx: commands.Context,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.triangle())

    @commands.command(name='blur', description="Shows the image as a blur.", usage="blur [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _blur(self, ctx: commands.Context,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.blur())

    @commands.command(name='rgb-graph', description="Shows the image with rgb graph.", usage="rgb-graph [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _rgb_graph(self, ctx: commands.Context,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.rgb())

    @commands.command(name='angel', description="Shows the image as a angel.", usage="angel [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _angel(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.angel())

    @commands.command(name='satan', description="Shows the image as satan.", usage="satan [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _satan(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.satan())

    @commands.command(name='delete', description="Shows the image as deleted.", usage="delete [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _delete(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.delete())

    @commands.command(name='fedora', description="Shows the image as tipped fedora.", usage="fedora [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _fedora(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.fedora())

    @commands.command(name='wanted', description="Shows the image as wanted.", usage="wanted [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wanted(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.wanted())

    @commands.command(name='stringify', description="Shows the image as stringifyed.", usage="stringify [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _stringify(self, ctx: commands.Context,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.stringify())

    @commands.command(name='mosiac', description="Shows the image as a mosiac.", usage="mosiac [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _mosiac(self, ctx: commands.Context,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.mosiac())

    @commands.command(name='sithlord', description="Shows the image as sithlord.", usage="sithlord [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sithlord(self, ctx: commands.Context,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.sith())

    @commands.command(name='jail', description="Shows the image in jail.", usage="jail [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _jail(self, ctx: commands.Context,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.jail())

    @commands.command(name='gay', description="Shows the image as gay.", usage="gay [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _gay(self, ctx: commands.Context,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.gay())

    @commands.command(name='trash', description="Shows the image as trash.", usage="trash [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _trash(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.trash())

    @commands.command(name='deepfry', description="Shows the image as deepfry.", usage="deepfry [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _deepfry(self, ctx: commands.Context,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.deepfry())

    @commands.command(name='ascii', description="Shows the image as ascii.", usage="ascii [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _ascii(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.ascii())

    @commands.command(name='charcoal', description="Shows the image as charcoal.", usage="charcoal [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _charcoal(self, ctx: commands.Context,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.charcoal())

    @commands.command(name='posterize', description="Shows the image as posterized.", usage="posterize [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _posterize(self, ctx: commands.Context,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.poster())

    @commands.command(name='sepia', description="Shows the image as sepia.", usage="sepia [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sepia(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.sepia())

    @commands.command(name='swirl', description="Shows the image as swirl.", usage="swirl [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _swirl(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.swirl())

    @commands.command(name='paint', description="Shows the image as painted.", usage="paint [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _paint(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.paint())

    @commands.command(name='night', description="Shows the image as night.", usage="night [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _night(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.night())

    @commands.command(name='rainbow', description="Shows the image as rainbow.", usage="rainbow [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _rainbow(self, ctx: commands.Context,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.rainbow())

    @commands.command(name='magik', description="Shows the image with magik.", usage="magik [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _magik(self, ctx: commands.Context,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, asyncdagpi.ImageFeatures.magik())

    @commands.command(name='flip', descripton="Flip an image.", usage="flip [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _flip(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        async with ctx.typing():
            with await imageToPIL(ctx, image) as image:
                new_image = image.rotate(180)

            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed)

    @commands.command(name='wide', descripton="Widen an image.", usage="wide [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wide(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        async with ctx.typing():
            with await imageToPIL(ctx, image) as image:
                new_image = image.resize((image.height*2, image.width))

            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed)

    @commands.command(name='squish', descripton="Squish an image.", usage="squish [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _squish(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        async with ctx.typing():
            with await imageToPIL(ctx, image) as image:
                new_image = image.resize((image.height, image.width*2))

            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed)


def setup(bot) -> None:
    bot.add_cog(Image(bot))
