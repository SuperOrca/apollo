# -*- coding: utf-8 -*-

"""
jishaku.features.shell
~~~~~~~~~~~~~~~~~~~~~~~~

The jishaku shell commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

from discord.ext import commands

from jishaku.codeblocks import Codeblock, codeblock_converter
from jishaku.exception_handling import ReplResponseReactor
from jishaku.features.baseclass import Feature
from jishaku.paginators import PaginatorInterface, WrappedPaginator
from jishaku.shell import ShellReader

from collections import Counter
from datetime import datetime


class SocketStats(Feature):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'socket_stats'):
            self.socket_stats = Counter()

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        self.bot.socket_stats[msg.get('t')] += 1

    @Feature.Command(parent="jsk", name="socketstats")
    async def jsk_socketstats(self, ctx: commands.Context):
        paginator = WrappedPaginator(prefix="```", max_size=1975)
        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        self.bot.loop.create_task(interface.send_to(ctx))

        delta = datetime.utcnow() - self.bot.uptime
        minutes = delta.total_seconds() / 60
        total = sum(self.socket_stats.values())
        cpm = total / minutes

        await interface.add_line(f'{total} socket events observed ({cpm:.2f}/minute):\n{self.socket_stats}')
