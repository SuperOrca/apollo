from discord.ext import commands


def check_hierarchy(ctx, member) -> None:
    if ctx.author.top_role < member.top_role:
        raise commands.BadArgument(
            "You do not have enough permissions to this.")
    if ctx.me.top_role < member.top_role:
        raise commands.BadArgument("I do not have enough permissions to this.")
