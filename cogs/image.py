from io import BytesIO
from typing import Union
from time import time

import asyncdagpi
import discord
from discord.ext import commands

from utils.context import ApolloContext
from utils.image import dagpi_process, imageToPIL, fileFromBytes, getImage, create_minecraft_blocks, process_minecraft


class Image(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        if not hasattr(bot, "minecraft_blocks"):
            self.bot.minecraft_blocks = {}
            self.bot.loop.create_task(create_minecraft_blocks(self.bot))

    @commands.command(name='pixelate', description="Shows the image as pixelated.", usage="pixelate [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _pixelate(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "pixel")

    @commands.command(name='colors', description="Shows the image's colors.", usage="colors [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _colors(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "colors")

    @commands.command(name='america', description="Shows the image as america.", usage="america [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _america(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "america")

    @commands.command(name='communism', description="Shows the image as communism.", usage="communism [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _communism(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "communism")

    @commands.command(name='triggered', description="Shows the image as triggered.", usage="triggered [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _triggered(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "triggered")

    @commands.command(name='wasted', description="Shows the image as wasted.", usage="wasted [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wasted(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "wasted")

    @commands.command(name='invert', description="Shows the image as inverted.", usage="invert [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _invert(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "invert")

    @commands.command(name='sobel', description="Shows the image as sobel.", usage="sobel [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sobel(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sobel")

    @commands.command(name='hog', description="Shows the image as a hog.", usage="hog [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _hog(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "hog")

    @commands.command(name='triangle', description="Shows the image as a triangle.", usage="triangle [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _triangle(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "triangle")

    @commands.command(name='blur', description="Shows the image as a blur.", usage="blur [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _blur(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "blur")

    @commands.command(name='rgb-graph', description="Shows the image with rgb graph.", usage="rgb-graph [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _rgb_graph(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "rgb")

    @commands.command(name='angel', description="Shows the image as a angel.", usage="angel [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _angel(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "angel")

    @commands.command(name='satan', description="Shows the image as satan.", usage="satan [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _satan(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "satan")

    @commands.command(name='delete', description="Shows the image as deleted.", usage="delete [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _delete(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "delete")

    @commands.command(name='fedora', description="Shows the image as tipped fedora.", usage="fedora [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _fedora(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "fedora")

    @commands.command(name='wanted', description="Shows the image as wanted.", usage="wanted [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wanted(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "wanted")

    @commands.command(name='stringify', description="Shows the image as stringifyed.", usage="stringify [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _stringify(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "stringify")

    @commands.command(name='mosiac', description="Shows the image as a mosiac.", usage="mosiac [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _mosiac(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "mosiac")

    @commands.command(name='sithlord', description="Shows the image as sithlord.", usage="sithlord [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sithlord(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sith")

    @commands.command(name='jail', description="Shows the image in jail.", usage="jail [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _jail(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "jail")

    @commands.command(name='gay', description="Shows the image as gay.", usage="gay [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _gay(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "gay")

    @commands.command(name='trash', description="Shows the image as trash.", usage="trash [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _trash(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "trash")

    @commands.command(name='deepfry', description="Shows the image as deepfry.", usage="deepfry [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _deepfry(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "deepfry")

    @commands.command(name='ascii', description="Shows the image as ascii.", usage="ascii [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _ascii(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "ascii")

    @commands.command(name='charcoal', description="Shows the image as charcoal.", usage="charcoal [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _charcoal(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "charcoal")

    @commands.command(name='posterize', description="Shows the image as posterized.", usage="posterize [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _posterize(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "poster")

    @commands.command(name='sepia', description="Shows the image as sepia.", usage="sepia [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sepia(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sepia")

    @commands.command(name='swirl', description="Shows the image as swirl.", usage="swirl [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _swirl(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "swirl")

    @commands.command(name='paint', description="Shows the image as painted.", usage="paint [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _paint(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "paint")

    @commands.command(name='night', description="Shows the image as night.", usage="night [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _night(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "night")

    @commands.command(name='rainbow', description="Shows the image as rainbow.", usage="rainbow [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _rainbow(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "rainbow")

    @commands.command(name='magik', description="Shows the image with magik.", usage="magik [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _magik(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "magik")

    @commands.command(name='sketch', description="Shows the image with sketch.", usage="sketch [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sketch(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sketch")

    @commands.command(name='shatter', description="Shows the image with shatter.", usage="shatter [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _shatter(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "shatter")

    @commands.command(name='polaroid', description="Shows the image with polaroid.", usage="shatter [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _polaroid(self, ctx: ApolloContext,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "polaroid")

    @commands.command(name='petpet', description="Shows the image with petpet.", usage="petpet [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _petpet(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "petpet")

    @commands.command(name='obama', description="Shows the image with obama.", usage="obama [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _obama(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "obama")

    @commands.command(name='neon', description="Shows the image with neon.", usage="neon [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _neon(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "neon")

    @commands.command(name='earth', description="Shows the image with earth.", usage="earth [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _earth(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "earth")

    @commands.command(name='dissolve', description="Shows the image with dissolve.", usage="dissolve [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _dissolve(self, ctx: ApolloContext,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "dissolve")

    @commands.command(name='cube', description="Shows the image with cube.", usage="cube [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _cube(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "cube")

    @commands.command(name='comic', description="Shows the image with comic.", usage="comic [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _comic(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "comic")

    @commands.command(name='bonk', description="Shows the image with bonk.", usage="bonk [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _bonk(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "bonk")

    @commands.command(name='bad', description="Shows the image with bad.", usage="bad [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _bad(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "bad")

    @commands.command(name='flip', descripton="Flip an image.", usage="flip [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _flip(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        with await imageToPIL(ctx, image) as image:
            new_image = image.rotate(180)
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {end-start:.2f} seconds")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='wide', descripton="Widen an image.", usage="wide [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _wide(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        with await imageToPIL(ctx, image) as image:
            new_image = image.resize((image.height * 2, image.width))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {end-start:.2f} seconds")

    @commands.command(name='ultrawide', descripton="Ultra widen an image.", usage="ultrawide [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _ultrawide(self, ctx: ApolloContext,
                         image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        with await imageToPIL(ctx, image) as image:
            new_image = image.resize((image.height * 4, image.width))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {end-start:.2f} seconds")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='squish', descripton="Squish an image.", usage="squish [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _squish(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        with await imageToPIL(ctx, image) as image:
            new_image = image.resize((image.height, image.width * 2))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {end-start:.2f} seconds")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='ultrasquish', descripton="Ultrasquish an image.", usage="ultrasquish [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _ultrasquish(self, ctx: ApolloContext,
                           image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        start = time()
        with await imageToPIL(ctx, image) as image:
            new_image = image.resize((image.height, image.width * 4))
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(text=f"Processed in {end-start:.2f} seconds")
        await ctx.reply(file=fileFromBytes(ctx, new_image), embed=embed, can_delete=True)

    @commands.command(name='minecraft', description="Get image as minecraft blocks.", usage="minecraft [image]",
                      aliases=['mc'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _minecraft(self, ctx: ApolloContext, image: Union[
            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        """
        Credits to The Anime Bot (https://github.com/Cryptex-github/the-anime-bot-bot) (ver cool dude)
        """
        url = await getImage(ctx, image)
        b = BytesIO(await (await self.bot.session.get(url)).read())
        start = time()
        file = discord.File(await process_minecraft(self.bot, b), f"{ctx.command.name}.png")
        end = time()
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_image(url=f"attachment://{ctx.command.name}.png")
        embed.set_footer(
            text=f"Processed in {end-start:.2f} seconds | Credits to The Anime Bot")
        await ctx.send(file=file,
                       embed=embed, can_delete=True)


def setup(bot) -> None:
    bot.add_cog(Image(bot))
