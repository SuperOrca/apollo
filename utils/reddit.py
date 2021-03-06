from config import VIEW_TIMEOUT
import random

import discord
from discord import ui
from discord.ext import commands

from utils.metrics import isImage, Embed


async def getpost(bot, ctx, subreddit) -> discord.Embed:
    """A method that fetches a post from a subreddit and returns an embed with a view."""

    async def post():
        embed = None
        i = 0
        while embed is None:
            try:
                data = await (await bot.session.get(f"https://www.reddit.com/r/{subreddit}/random/.json")).json()
                posts = data[0]['data']['children']
                num = (len(posts) - 1)
                post = posts[random.randint(0, num)]['data']
                if post['over_18'] and not ctx.channel.nsfw:
                    embed = None
                elif not isImage(post['url']):
                    embed = None
                else:
                    embed = Embed(title=post['title'], url=f"https://www.reddit.com{post['permalink']}")
                    embed.set_image(url=post['url'])
                    embed.set_footer(
                        text=f"👍 {post['ups']} 💬 {post['num_comments']}")
            except KeyError as e:
                embed = None
            i += 1
            if i >= 5:
                raise commands.UserInputError(
                    f"Could not find a image from `{subreddit}`.")
        return embed

    class RedditView(ui.View):
        def __init__(self):
            super().__init__(timeout=VIEW_TIMEOUT)

        async def interaction_check(self, interaction: discord.Interaction):
            if not self.ctx.author == interaction.user:
                await interaction.response.send_message(
                    f"This view is owned by {self.ctx.author.mention}. You make your own view by using the `{self.ctx.command}` command.",
                    ephemeral=True)
                return False
            return True

        @ui.button(emoji='⬅️', style=discord.ButtonStyle.secondary)
        async def previous(self, button: ui.Button, interaction: discord.Interaction):
            if self.num > 0:
                self.num -= 1
                await interaction.message.edit(embed=self.log[self.num])
            else:
                await interaction.response.send_message("Cannot go to previous.", ephemeral=True)

        @ui.button(emoji='⏹️', style=discord.ButtonStyle.secondary)
        async def on_stop(self, button: ui.Button, interaction: discord.Interaction):
            await self.ctx.tick()
            self.stop()
            await interaction.message.delete()

        @ui.button(emoji='➡️', style=discord.ButtonStyle.secondary)
        async def forwards(self, button: ui.Button, interaction: discord.Interaction):
            self.num += 1
            try:
                await interaction.message.edit(embed=self.log[self.num])
            except IndexError:
                try:
                    embed = await post()
                except commands.BadArgument:
                    self.on_stop(button, interaction)
                self.log.append(embed)
                await interaction.message.edit(embed=embed)

        @classmethod
        async def start(cls):
            cls.ctx = ctx
            cls.log = []
            cls.num = 0
            embed = await post()
            cls.log.append(embed)
            await ctx.reply(embed=embed, view=cls())

    return RedditView
