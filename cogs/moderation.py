import asyncio
from typing import Optional
from utils.metrics import Embed

import discord
from discord.ext import commands

from utils.checks import check_hierarchy
from utils.context import ApolloContext


class Moderation(commands.Cog):
	def __init__(self, bot) -> None:
		self.bot = bot
		self._cd_type = commands.BucketType.user
		self._cd = commands.CooldownMapping.from_cooldown(
			1, 2.5, self._cd_type)

	async def cog_check(self, ctx: ApolloContext):
		bucket = self._cd.get_bucket(ctx.message)
		retry_after = bucket.update_rate_limit()
		if retry_after:
			raise commands.CommandOnCooldown(
				self._cd, retry_after, self._cd_type)
		else:
			return True

	@commands.command(name='purge', description="Clean up messages in a channel.", aliases=['clear'],
					  usage="<limit> [channel]")
	@commands.has_guild_permissions(manage_messages=True)
	@commands.bot_has_guild_permissions(manage_messages=True)
	async def _purge(self, ctx: ApolloContext, limit: int, channel: Optional[commands.TextChannelConverter] = None) -> None:
		if limit < 1 or limit > 100:
			raise commands.CommandError("Limit must been between 1 and 100.")

		channel = channel or ctx.channel
		msgs = await channel.purge(limit=limit)
		await asyncio.sleep(1)
		await ctx.send(can_delete=True,
					   embed=Embed(description=f"Cleared `{len(msgs)}` messages."))

	@commands.command(name='ban', description="Ban a member.", usage="<member> [reason]")
	@commands.has_guild_permissions(ban_members=True)
	@commands.bot_has_guild_permissions(ban_members=True)
	async def _ban(self, ctx: ApolloContext, member: commands.MemberConverter, *, reason: Optional[commands.clean_content] = None) -> None:
		check_hierarchy(ctx, member)
		reason = reason or "no reason provided"
		try:
			await member.send(embed=Embed(
				description=f"You have been banned from `{ctx.guild.name}** for **{reason}` by {ctx.author.mention}."))
		except discord.HTTPException:
			...
		await member.ban(reason=reason)
		await ctx.reply(
			embed=Embed(description=f"Banned {member.mention} for `{reason}`. (by {ctx.author.mention})"))

	@commands.command(name='kick', description="Kick a member.", usage="<member> [reason]")
	@commands.has_guild_permissions(kick_members=True)
	@commands.bot_has_guild_permissions(kick_members=True)
	async def _kick(self, ctx: ApolloContext, member: commands.MemberConverter, *, reason: Optional[commands.clean_content] = None) -> None:
		check_hierarchy(ctx, member)
		reason = reason or "no reason provided"
		try:
			await member.send(embed=Embed(
				description=f"You have been kicked from `{ctx.guild.name}** for **{reason}` by {ctx.author.mention}."))
		except discord.HTTPException:
			...
		await member.kick(reason=reason)
		await ctx.reply(
			embed=Embed(description=f"Kicked {member.mention} for `{reason}`. (by {ctx.author.mention})"))

	@commands.command(name='slowmode', description="Edit slowmode of channel.", usage="<seconds>",
					  aliases=['sm'])
	@commands.has_guild_permissions(manage_messages=True)
	@commands.bot_has_guild_permissions(manage_messages=True)
	async def _slowmode(self, ctx: ApolloContext, seconds: int, channel: Optional[commands.TextChannelConverter] = None) -> None:
		if seconds < 0 or seconds > 21600:
			raise commands.CommandError(
				"Slowmode must been between 0 and 21,600.")

		channel = channel or ctx.channel
		await ctx.channel.edit(slowmode_delay=seconds)
		await ctx.reply(embed=Embed(
			description=f"Set slowmode of {channel.mention} to `{seconds}` seconds."))

	@commands.command(name='unban', description="Unban a user.", usage="<user>")
	@commands.has_guild_permissions(ban_members=True)
	@commands.bot_has_guild_permissions(ban_members=True)
	async def _unban(self, ctx: ApolloContext, user: commands.UserConverter) -> None:
		member = discord.Object(id=user.id)
		await ctx.guild.unban(member)
		await ctx.reply(embed=Embed(description=f"Unbanned {user.mention} (by {ctx.author.mention})."))

	@commands.command(name='setnick', description="Set nick of member. Set to 'reset' to reset.",
					  usage="<member> <nick>")
	@commands.has_guild_permissions(manage_nicknames=True)
	@commands.bot_has_guild_permissions(manage_nicknames=True)
	async def _setnick(self, ctx: ApolloContext, member: commands.MemberConverter, nick: commands.clean_content):
		check_hierarchy(ctx, member)
		if nick == "reset":
			await member.edit(nick=None)
		else:
			await member.edit(nick=nick)
		await ctx.reply(embed=Embed(description=f"Changed {member.mention} nickname to `{nick}`."))


def setup(bot) -> None:
	bot.add_cog(Moderation(bot))
