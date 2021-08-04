import discord
from discord.ext import commands

import asyncio
import functools

__all__ = ("executor", "moderator", "administrator", "helper")


def executor(loop=None):
    """Stolen from https://github.com/InterStella0/stella_bot/"""
    loop = loop or asyncio.get_event_loop()

    def inner_function(func):
        @functools.wraps(func)
        def function(*args, **kwargs):
            partial = functools.partial(func, *args, **kwargs)
            return loop.run_in_executor(None, partial)

        return function

    return inner_function


def helper():
    async def predicate(ctx):
        permissions = ctx.author.guild_permissions
        if (
            permissions.manage_nicknames
            or permissions.administrator
            or ctx.author.id == ctx.guild.owner_id
            or ctx.author.id in ctx.bot.owner_ids
        ):
            return True
        else:
            raise commands.MissingPermissions("manage_nicknames")
        return False

    return commands.check(predicate)


def moderator():
    async def predicate(ctx):
        permissions = ctx.author.guild_permissions
        if (
            permissions.ban_members
            or permissions.administrator
            or ctx.author.id == ctx.guild.owner_id
            or ctx.author.id in ctx.bot.owner_ids
        ):
            return True
        else:
            raise commands.MissingPermissions("ban_members")
        return False

    return commands.check(predicate)


def administrator():
    async def predicate(ctx):
        if (
            ctx.author.guild_permissions.administrator
            or ctx.author.id == ctx.guild.owner_id
            or ctx.author.id in ctx.bot.owner_ids
        ):
            return True
        else:
            return commands.MissingPermissions("administrator")

    return commands.check(predicate)