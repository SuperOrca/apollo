from os import getenv
from typing import Union
from io import BytesIO

import asyncdagpi
import discord
from discord.ext import commands
import numpy as np
import os
import aiofile
from PIL import Image as Im
from PIL import UnidentifiedImageError

from utils.image import dagpi_process, imageToPIL, fileFromBytes, getImage
from utils.decorators import asyncexe


class Image(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        if not hasattr(bot, "minecraft_blocks"):
            self.bot.minecraft_blocks = {}
            self.bot.loop.create_task(self.create_minecraft_blocks())

    async def create_minecraft_blocks(self):
        for _file in os.listdir("assets/minecraft_blocks"):
            async with aiofile.async_open("assets/minecraft_blocks/" + _file, "rb") as afp:
                b = await afp.read()
                await self.resize_and_save_minecraft_blocks(BytesIO(b))

    async def resize_and_save_minecraft_blocks(self, b):
        try:
            with Im.open(b) as image:
                image = image.convert("RGBA")
                self.bot.minecraft_blocks[image.resize(
                    (1, 1)).getdata()[0]] = image
        except UnidentifiedImageError:
            pass

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

    @commands.command(name='commoncolor', description="Get the most common color in an image.", usage="commoncolor [image]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _commoncolor(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None):
        async with ctx.typing():
            def frequency(my_list):
                freq = {}
                for item in my_list:
                    if item in freq:
                        freq[item] += 1
                    else:
                        freq[item] = 1
                return sorted(freq, key=lambda k: freq[k], reverse=True)

            url = await getImage(ctx, image)
            response = await self.bot.session.get(url)

            with Im.open(BytesIO(await response.read())) as image:
                palette = image.getpalette()

            frequent = frequency([f"#{r:02x}{g:02x}{b:02x}" for r, g, b in [
                                 tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]])

            embed = discord.Embed(
                title="Common Color: " + frequent[0], color=int(f"0x{frequent[0].strip('#')}", 16))
            embed.set_image(
                url=f"https://some-random-api.ml/canvas/colorviewer?hex={frequent[0].strip('#')}")
            embed.set_thumbnail(url=url)
            await ctx.reply(embed=embed)

    @asyncexe
    def process_minecraft(self, b: BytesIO) -> BytesIO:
        minecraft_array = np.array(list(self.bot.minecraft_blocks.keys()))
        np.expand_dims(minecraft_array, axis=-1)
        image = Im.open(b)
        image = image.convert("RGBA").resize((64, 64))
        with Im.new("RGBA", (image.width * 16, image.height * 16)) as final_image:
            arr = np.asarray(image)
            np.expand_dims(arr, axis=-1)
            for y, r in enumerate(arr):
                for x, c in enumerate(r):
                    difference = np.sqrt(
                        np.sum((minecraft_array - c) ** 2, axis=1))
                    where = np.where(difference == np.amin(difference))
                    to_paste = self.bot.minecraft_blocks[tuple(
                        minecraft_array[where][0])]
                    final_image.paste(to_paste, (x * 16, y * 16), to_paste)
        buffer = BytesIO()
        final_image.save(buffer, "PNG")
        buffer.seek(0)
        return buffer

    @commands.command(name='minecraft', description="Get image as minecraft blocks.", usage="minecraft [image]", aliases=['mc'])
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def _minecraft(self, ctx: commands.Context, image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        async with ctx.typing():
            url = await getImage(ctx, image)
            b = BytesIO(await (await self.bot.session.get(url)).read())
            await ctx.send(file=discord.File(await self.process_minecraft(b), "minecraft.png"))


def setup(bot) -> None:
    bot.add_cog(Image(bot))
