import discord
from discord.ext import commands
from utils.image import dagpi_process
from utils.context import ApolloContext
from typing import Union


class Dagpi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd_type = commands.BucketType.user
        self._cd = commands.CooldownMapping.from_cooldown(1, 7., self._cd_type)

    async def cog_check(self, ctx: ApolloContext):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(self._cd, retry_after, self._cd_type)
        else:
            return True

    @commands.command(name='pixelate', description="Shows the image as pixelated.", usage="pixelate [image]")
    async def _pixelate(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "pixel")

    @commands.command(name='colors', description="Shows the image's colors.", usage="colors [image]")
    async def _colors(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "colors")

    @commands.command(name='america', description="Shows the image as america.", usage="america [image]")
    async def _america(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "america")

    @commands.command(name='communism', description="Shows the image as communism.", usage="communism [image]")
    async def _communism(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "communism")

    @commands.command(name='triggered', description="Shows the image as triggered.", usage="triggered [image]")
    async def _triggered(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "triggered")

    @commands.command(name='wasted', description="Shows the image as wasted.", usage="wasted [image]")
    async def _wasted(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "wasted")

    @commands.command(name='invert', description="Shows the image as inverted.", usage="invert [image]")
    async def _invert(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "invert")

    @commands.command(name='sobel', description="Shows the image as sobel.", usage="sobel [image]")
    async def _sobel(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sobel")

    @commands.command(name='hog', description="Shows the image as a hog.", usage="hog [image]")
    async def _hog(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "hog")

    @commands.command(name='triangle', description="Shows the image as a triangle.", usage="triangle [image]")
    async def _triangle(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "triangle")

    @commands.command(name='rgb-graph', description="Shows the image with rgb graph.", usage="rgb-graph [image]")
    async def _rgb_graph(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "rgb")

    @commands.command(name='angel', description="Shows the image as a angel.", usage="angel [image]")
    async def _angel(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "angel")

    @commands.command(name='satan', description="Shows the image as satan.", usage="satan [image]")
    async def _satan(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "satan")

    @commands.command(name='delete', description="Shows the image as deleted.", usage="delete [image]")
    async def _delete(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "delete")

    @commands.command(name='fedora', description="Shows the image as tipped fedora.", usage="fedora [image]")
    async def _fedora(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "fedora")

    @commands.command(name='wanted', description="Shows the image as wanted.", usage="wanted [image]")
    async def _wanted(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "wanted")

    @commands.command(name='stringify', description="Shows the image as stringifyed.", usage="stringify [image]")
    async def _stringify(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "stringify")

    @commands.command(name='mosiac', description="Shows the image as a mosiac.", usage="mosiac [image]")
    async def _mosiac(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "mosiac")

    @commands.command(name='sithlord', description="Shows the image as sithlord.", usage="sithlord [image]")
    async def _sithlord(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sith")

    @commands.command(name='jail', description="Shows the image in jail.", usage="jail [image]")
    async def _jail(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "jail")

    @commands.command(name='gay', description="Shows the image as gay.", usage="gay [image]")
    async def _gay(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "gay")

    @commands.command(name='trash', description="Shows the image as trash.", usage="trash [image]")
    async def _trash(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "trash")

    @commands.command(name='deepfry', description="Shows the image as deepfry.", usage="deepfry [image]")
    async def _deepfry(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "deepfry")

    @commands.command(name='ascii', description="Shows the image as ascii.", usage="ascii [image]")
    async def _ascii(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "ascii")

    @commands.command(name='charcoal', description="Shows the image as charcoal.", usage="charcoal [image]")
    async def _charcoal(self, ctx: ApolloContext,
                        image: Union[
                            discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "charcoal")

    @commands.command(name='posterize', description="Shows the image as posterized.", usage="posterize [image]")
    async def _posterize(self, ctx: ApolloContext,
                         image: Union[
                             discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "poster")

    @commands.command(name='sepia', description="Shows the image as sepia.", usage="sepia [image]")
    async def _sepia(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sepia")

    @commands.command(name='paint', description="Shows the image as painted.", usage="paint [image]")
    async def _paint(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "paint")

    @commands.command(name='night', description="Shows the image as night.", usage="night [image]")
    async def _night(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "night")

    @commands.command(name='rainbow', description="Shows the image as rainbow.", usage="rainbow [image]")
    async def _rainbow(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "rainbow")

    @commands.command(name='magik', description="Shows the image with magik.", usage="magik [image]")
    async def _magik(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "magik")

    @commands.command(name='sketch', description="Shows the image with sketch.", usage="sketch [image]")
    async def _sketch(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "sketch")

    @commands.command(name='shatter', description="Shows the image with shatter.", usage="shatter [image]")
    async def _shatter(self, ctx: ApolloContext,
                       image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "shatter")

    @commands.command(name='polaroid', description="Shows the image with polaroid.", usage="shatter [image]")
    async def _polaroid(self, ctx: ApolloContext,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "polaroid")

    @commands.command(name='petpet', description="Shows the image with petpet.", usage="petpet [image]")
    async def _petpet(self, ctx: ApolloContext,
                      image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "petpet")

    @commands.command(name='obama', description="Shows the image with obama.", usage="obama [image]")
    async def _obama(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "obama")

    @commands.command(name='neon', description="Shows the image with neon.", usage="neon [image]")
    async def _neon(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "neon")

    @commands.command(name='earth', description="Shows the image with earth.", usage="earth [image]")
    async def _earth(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "earth")

    @commands.command(name='dissolve', description="Shows the image with dissolve.", usage="dissolve [image]")
    async def _dissolve(self, ctx: ApolloContext,
                        image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "dissolve")

    @commands.command(name='cube', description="Shows the image with cube.", usage="cube [image]")
    async def _cube(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "cube")

    @commands.command(name='comic', description="Shows the image with comic.", usage="comic [image]")
    async def _comic(self, ctx: ApolloContext,
                     image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "comic")

    @commands.command(name='bonk', description="Shows the image with bonk.", usage="bonk [image]")
    async def _bonk(self, ctx: ApolloContext,
                    image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "bonk")

    @commands.command(name='bad', description="Shows the image with bad.", usage="bad [image]")
    async def _bad(self, ctx: ApolloContext,
                   image: Union[discord.Emoji, discord.PartialEmoji, commands.MemberConverter, str] = None) -> None:
        await dagpi_process(ctx, image, "bad")


def setup(bot):
    bot.add_cog(Dagpi(bot))
