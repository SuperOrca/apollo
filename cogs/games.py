import discord
from Discord_Games import typeracer
from discord.ext import commands
from utils.games.tictactoe import TicTacToe


class Games(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='typeracer', description="Typeracer game!")
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def _typeracer(self, ctx) -> None:
        game = typeracer.TypeRacer()

        await game.start(ctx, embed_color=0x2F3136, show_author=False,
                         path_to_text_font='/usr/share/fonts/truetype/freefont/FreeSans.ttf', timeout=60.)


def setup(bot) -> None:
    bot.add_cog(Games(bot))
