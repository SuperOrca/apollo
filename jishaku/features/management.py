# -*- coding: utf-8 -*-

"""
jishaku.features.management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The jishaku extension and bot control commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import itertools
import math
import time
import traceback
import json
from typing import Optional

import aiofile
from discord.ext import commands

from jishaku.features.baseclass import Feature
from jishaku.flags import JISHAKU_USE_BRAILLE_J
from jishaku.modules import ExtensionConverter
from jishaku.paginators import WrappedPaginator


class ManagementFeature(Feature):
    """
    Feature containing the extension and bot control commands
    """

    @Feature.Command(parent="jsk", name="load", aliases=["reload"])
    async def jsk_load(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Loads or reloads the given extension names.

        Reports any extensions that failed to load.
        """

        paginator = WrappedPaginator(prefix='', suffix='')

        # 'jsk reload' on its own just reloads jishaku
        if ctx.invoked_with == 'reload' and not extensions:
            extensions = [['jishaku']]

        for extension in itertools.chain(*extensions):
            method, icon = (
                (self.bot.reload_extension,
                 "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}")
                if extension in self.bot.extensions else
                (self.bot.load_extension, "\N{INBOX TRAY}")
            )

            try:
                method(extension)
            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = ''.join(traceback.format_exception(
                    type(exc), exc, exc.__traceback__, 1))

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.reply(page)

    @Feature.Command(parent="jsk", name="unload")
    async def jsk_unload(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Unloads the given extension names.

        Reports any extensions that failed to unload.
        """

        paginator = WrappedPaginator(prefix='', suffix='')
        icon = "\N{OUTBOX TRAY}"

        for extension in itertools.chain(*extensions):
            try:
                self.bot.unload_extension(extension)
            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = "".join(traceback.format_exception(
                    type(exc), exc, exc.__traceback__, 1))

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.reply(page)

    @Feature.Command(parent="jsk", name="shutdown", aliases=["logout"])
    async def jsk_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """

        ellipse_character = "\N{BRAILLE PATTERN DOTS-356}" if JISHAKU_USE_BRAILLE_J else "\N{HORIZONTAL ELLIPSIS}"

        await ctx.reply(f"Logging out now{ellipse_character}")
        await ctx.bot.close()

    @Feature.Command(parent="jsk", name="grammar")
    async def jsk_grammar(self, ctx: commands.Context, *, text: str):
        await ctx.send(''.join(char.upper() if index % 2 == 0 else char.lower() for index, char in enumerate(text, start=1)))

    @Feature.Command(parent="jsk", name="socketstats")
    async def jsk_socketstats(self, ctx: commands.Context):
        await ctx.reply(f"```\n{json.dumps({key: value for key, value in sorted(dict(ctx.bot.socket_stats).items(), reverse=True, key=lambda item: item[1])}, indent=4)}\n```")

    @Feature.Command(parent="jsk", name="blacklist")
    async def jsk_blacklist(self, ctx: commands.Context, mode: str, user: Optional[commands.UserConverter] = None):
        if mode == "list":
            async with aiofile.async_open("blacklist.json") as afp:
                data = json.loads(await afp.readlines())
            data = [f"`{self.bot.get_user(line.strip())}`" for line in data]
            await ctx.reply(', '.join(data))
        elif mode == "add":
            async with aiofile.async_open("blacklist.json") as afp:
                data = json.loads(await afp.readlines())
            async with aiofile.async_open("blacklist.json", 'w') as afp:
                await afp.write(data.append(user.id))
        elif mode == "remove":
            async with aiofile.async_open("blacklist.json") as afp:
                data = json.loads(await afp.readlines())
            async with aiofile.async_open("blacklist.json", 'w') as afp:
                await afp.write(data.remove(user.id))

    @Feature.Command(parent="jsk", name="rtt", aliases=["ping"])
    async def jsk_rtt(self, ctx: commands.Context):
        """
        Calculates Round-Trip Time to the API.
        """

        message = None

        # We'll show each of these readings as well as an average and standard deviation.
        api_readings = []
        # We'll also record websocket readings, but we'll only provide the average.
        websocket_readings = []

        # We do 6 iterations here.
        # This gives us 5 visible readings, because a request can't include the stats for itself.
        for _ in range(6):
            # First generate the text
            text = "Calculating round-trip time...\n\n"
            text += "\n".join(
                f"Reading {index + 1}: {reading * 1000:.2f}ms" for index, reading in enumerate(api_readings))

            if api_readings:
                average = sum(api_readings) / len(api_readings)

                if len(api_readings) > 1:
                    stddev = math.sqrt(
                        sum(math.pow(reading - average, 2) for reading in api_readings) / (len(api_readings) - 1))
                else:
                    stddev = 0.0

                text += f"\n\nAverage: {average * 1000:.2f} \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms"
            else:
                text += "\n\nNo readings yet."

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\nWebsocket latency: {average * 1000:.2f}ms"
            else:
                text += f"\nWebsocket latency: {self.bot.latency * 1000:.2f}ms"

            before = time.perf_counter()
            # Now do the actual request and reading
            if message:
                await message.edit(content=text)
            else:
                message = await ctx.reply(content=text)
            after = time.perf_counter()

            api_readings.append(after - before)
            # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)
