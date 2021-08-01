from utils.context import ApolloContext
import discord
from discord.ext import commands


def check_hierarchy(ctx: ApolloContext, member: discord.Member) -> None:
	"""A method that checks if the moderator and bot has a higher role than the member."""
	if ctx.author.top_role < member.top_role:
		raise commands.BadArgument(
			"You do not have enough permissions to this.")
	if ctx.me.top_role < member.top_role:
		raise commands.BadArgument("I do not have enough permissions to this.")
