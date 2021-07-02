import asyncio

import discord
from discord.ext import commands

from utils.checks import check_hierarchy


class Mod(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='purge', description="Clean up messages in a channel.", aliases=['clear'],
                      usage="purge <limit> [channel]")
    @commands.has_guild_permissions(manage_messages=True)
    async def _purge(self, ctx, limit: int, channel: commands.TextChannelConverter = None) -> None:
        if limit < 1 or limit > 100:
            raise commands.BadArgument("Limit must been between 1 and 100.")

        channel = channel or ctx.channel
        await channel.purge(limit=limit)
        await asyncio.sleep(1)
        m = await ctx.send(
            embed=discord.Embed(description=f"Cleared `{limit}` messages.", color=discord.Color.dark_red()))
        await asyncio.sleep(5)
        await m.delete()

    @commands.command(name='ban', description="Ban a member.", usage="ban <member> [reason]")
    @commands.has_guild_permissions(ban_members=True)
    async def _ban(self, ctx, member: commands.MemberConverter, *, reason: str = None) -> None:
        check_hierarchy(ctx.author, member)
        reason = reason or "no reason provided"
        try:
            await member.send(embed=discord.Embed(
                description=f"You have been banned from `{ctx.guild.name}** for **{reason}` by {ctx.author.mention}.",
                color=member.color))
        except discord.HTTPException:
            ...
        await member.ban(reason=reason)
        await ctx.reply(
            embed=discord.Embed(description=f"Banned {member.mention} for `{reason}`. (by {ctx.author.mention})",
                                color=discord.Color.dark_red()))

    @commands.command(name='kick', description="Kick a member.", usage="kick <member> [reason]")
    @commands.has_guild_permissions(kick_members=True)
    async def _kick(self, ctx, member: commands.MemberConverter, *, reason: str = None) -> None:
        check_hierarchy(ctx.author, member)
        reason = reason or "no reason provided"
        try:
            await member.send(embed=discord.Embed(
                description=f"You have been kicked from `{ctx.guild.name}** for **{reason}` by {ctx.author.mention}.",
                color=member.color))
        except discord.HTTPException:
            ...
        await member.kick(reason=reason)
        await ctx.reply(
            embed=discord.Embed(description=f"Kicked {member.mention} for `{reason}`. (by {ctx.author.mention})",
                                color=discord.Color.dark_red()))

    @commands.command(name='slowmode', description="Edit slowmode of channel.", usage="slowmode <seconds>",
                      aliases=['sm'])
    @commands.has_guild_permissions(manage_messages=True)
    async def _slowmode(self, ctx, seconds: int, channel: commands.TextChannelConverter = None) -> None:
        if seconds < 0 or seconds > 21600:
            raise commands.BadArgument(
                "Slowmode must been between 0 and 21,600.")

        channel = channel or ctx.channel
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(embed=discord.Embed(
            description=f"Set slowmode of {channel.mention} to `{seconds}` seconds.", color=discord.Color.dark_red()))

    @commands.command(name='unban', description="Unban a user.", usage="unban <user>")
    @commands.has_guild_permissions(manage_messages=True)
    async def _unban(self, ctx, user: commands.UserConverter) -> None:
        member = discord.Object(id=user.id)
        await ctx.guild.unban(member)
        await ctx.reply(embed=discord.Embed(description=f"Unbanned {user.mention} (by {ctx.author.mention}).",
                                            color=discord.Color.dark_red()))

    @commands.command(name='setnick', description="Set nick of member. Set to 'reset' to reset.",
                      usage="nick <member> <nick>")
    @commands.has_guild_permissions(manage_nicknames=True)
    async def _setnick(self, ctx, member: commands.MemberConverter, nick: str):
        check_hierarchy(ctx.author, member)
        if nick == "reset":
            await member.edit(nick=None)
        else:
            await member.edit(nick=nick)
        await ctx.reply(embed=discord.Embed(description=f"Changed {member.mention} nickname to `{nick}`.",
                                            color=discord.Color.dark_red()))


def setup(bot) -> None:
    bot.add_cog(Mod(bot))
