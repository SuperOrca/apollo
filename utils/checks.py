import discord
from discord.ext import commands

from utils.context import ApolloContext


def check_hierarchy(ctx: ApolloContext, member: discord.Member) -> None:
    """A method that checks if the moderator and bot has a higher role than the member."""
    if ctx.author.top_role < member.top_role:
        raise commands.CommandError(
            "You do not have enough permissions to this.")
    if ctx.me.top_role < member.top_role:
        raise commands.CommandError("I do not have enough permissions to this.")
