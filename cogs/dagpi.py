from inspect import Parameter
from typing import Optional

from discord.ext import commands

from utils.context import ApolloContext
from utils.converters import ImageConverter
from utils.image import dagpi_process

_old_transform = commands.Command.transform


def _transform(self, ctx, param):
    if param.annotation is Optional[ImageConverter]:
        loop = ctx.bot.loop
        if ctx.message.attachments:
            param = Parameter(
                param.name, param.kind, default=loop.run_until_complete(ImageConverter().convert(ctx, ctx.message.attachments[0].url)), annotation=ImageConverter)
        else:
            param = Parameter(
                param.name, param.kind, default=loop.run_until_complete(ImageConverter().convert(ctx, ctx.author.avatar.url)), annotation=ImageConverter)

    return _old_transform(self, ctx, param)


commands.Command.transform = _transform


class Dagpi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

    @commands.command(name='pixelate', description="Shows the image as pixelated.", usage="[image]")
    async def _pixelate(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "pixel")

    @commands.command(name='colors', description="Shows the image's colors.", usage="[image]")
    async def _colors(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "colors")

    @commands.command(name='america', description="Shows the image as america.", usage="[image]")
    async def _america(self, ctx: ApolloContext,
                       image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "america")

    @commands.command(name='communism', description="Shows the image as communism.", usage="[image]")
    async def _communism(self, ctx: ApolloContext,
                         image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "communism")

    @commands.command(name='triggered', description="Shows the image as triggered.", usage="[image]")
    async def _triggered(self, ctx: ApolloContext,
                         image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "triggered")

    @commands.command(name='wasted', description="Shows the image as wasted.", usage="[image]")
    async def _wasted(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "wasted")

    @commands.command(name='invert', description="Shows the image as inverted.", usage="[image]")
    async def _invert(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "invert")

    @commands.command(name='sobel', description="Shows the image as sobel.", usage="[image]")
    async def _sobel(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "sobel")

    @commands.command(name='hog', description="Shows the image as a hog.", usage="[image]")
    async def _hog(self, ctx: ApolloContext,
                   image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "hog")

    @commands.command(name='triangle', description="Shows the image as a triangle.", usage="[image]")
    async def _triangle(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "triangle")

    @commands.command(name='rgb-graph', description="Shows the image with rgb graph.", usage="[image]")
    async def _rgb_graph(self, ctx: ApolloContext,
                         image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "rgb")

    @commands.command(name='angel', description="Shows the image as a angel.", usage="[image]")
    async def _angel(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "angel")

    @commands.command(name='satan', description="Shows the image as satan.", usage="[image]")
    async def _satan(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "satan")

    @commands.command(name='delete', description="Shows the image as deleted.", usage="[image]")
    async def _delete(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "delete")

    @commands.command(name='fedora', description="Shows the image as tipped fedora.", usage="[image]")
    async def _fedora(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "fedora")

    @commands.command(name='wanted', description="Shows the image as wanted.", usage="[image]")
    async def _wanted(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "wanted")

    @commands.command(name='stringify', description="Shows the image as stringifyed.", usage="[image]")
    async def _stringify(self, ctx: ApolloContext,
                         image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "stringify")

    @commands.command(name='mosiac', description="Shows the image as a mosiac.", usage="[image]")
    async def _mosiac(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "mosiac")

    @commands.command(name='sithlord', description="Shows the image as sithlord.", usage="[image]")
    async def _sithlord(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "sith")

    @commands.command(name='jail', description="Shows the image in jail.", usage="[image]")
    async def _jail(self, ctx: ApolloContext,
                    image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "jail")

    @commands.command(name='gay', description="Shows the image as gay.", usage="[image]")
    async def _gay(self, ctx: ApolloContext,
                   image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "gay")

    @commands.command(name='trash', description="Shows the image as trash.", usage="[image]")
    async def _trash(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "trash")

    @commands.command(name='deepfry', description="Shows the image as deepfry.", usage="[image]")
    async def _deepfry(self, ctx: ApolloContext,
                       image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "deepfry")

    @commands.command(name='ascii', description="Shows the image as ascii.", usage="[image]")
    async def _ascii(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "ascii")

    @commands.command(name='charcoal', description="Shows the image as charcoal.", usage="[image]")
    async def _charcoal(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "charcoal")

    @commands.command(name='posterize', description="Shows the image as posterized.", usage="[image]")
    async def _posterize(self, ctx: ApolloContext,
                         image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "poster")

    @commands.command(name='sepia', description="Shows the image as sepia.", usage="[image]")
    async def _sepia(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "sepia")

    @commands.command(name='paint', description="Shows the image as painted.", usage="[image]")
    async def _paint(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "paint")

    @commands.command(name='night', description="Shows the image as night.", usage="[image]")
    async def _night(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "night")

    @commands.command(name='rainbow', description="Shows the image as rainbow.", usage="[image]")
    async def _rainbow(self, ctx: ApolloContext,
                       image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "rainbow")

    @commands.command(name='magik', description="Shows the image with magik.", usage="[image]")
    async def _magik(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "magik")

    @commands.command(name='sketch', description="Shows the image with sketch.", usage="[image]")
    async def _sketch(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "sketch")

    @commands.command(name='shatter', description="Shows the image with shatter.", usage="[image]")
    async def _shatter(self, ctx: ApolloContext,
                       image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "shatter")

    @commands.command(name='polaroid', description="Shows the image with polaroid.", usage="[image]")
    async def _polaroid(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "polaroid")

    @commands.command(name='petpet', description="Shows the image with petpet.", usage="[image]")
    async def _petpet(self, ctx: ApolloContext,
                      image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "petpet")

    @commands.command(name='obama', description="Shows the image with obama.", usage="[image]")
    async def _obama(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "obama")

    @commands.command(name='neon', description="Shows the image with neon.", usage="[image]")
    async def _neon(self, ctx: ApolloContext,
                    image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "neon")

    @commands.command(name='earth', description="Shows the image with earth.", usage="[image]")
    async def _earth(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "earth")

    @commands.command(name='dissolve', description="Shows the image with dissolve.", usage="[image]")
    async def _dissolve(self, ctx: ApolloContext,
                        image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "dissolve")

    @commands.command(name='cube', description="Shows the image with cube.", usage="[image]")
    async def _cube(self, ctx: ApolloContext,
                    image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "cube")

    @commands.command(name='comic', description="Shows the image with comic.", usage="[image]")
    async def _comic(self, ctx: ApolloContext,
                     image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "comic")

    @commands.command(name='bonk', description="Shows the image with bonk.", usage="[image]")
    async def _bonk(self, ctx: ApolloContext,
                    image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "bonk")

    @commands.command(name='bad', description="Shows the image with bad.", usage="[image]")
    async def _bad(self, ctx: ApolloContext,
                   image: Optional[ImageConverter]) -> None:
        await dagpi_process(ctx, image.url, "bad")


def setup(bot):
    bot.add_cog(Dagpi(bot))
