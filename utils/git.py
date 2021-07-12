import itertools
import datetime
import humanize

from .decorators import asyncexe


def format_commit(commit):
    commit = commit["commit"]
    return f"`[click]({commit['url']})` {commit['message']}"


async def get_last_commits(bot, count=3):
    commits = await (await bot.session.get("https://api.github.com/repos/SuperOrca/apollo/commits")).json()
    return '\n'.join(format_commit(c) for c in commits[:count])
