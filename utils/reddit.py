import random

import discord
from discord import ui
from discord.ext import commands

from utils.context import ApolloContext
from utils.metrics import isImage


async def getpost(bot, channel, subreddit) -> discord.Embed:
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
                if post['over_18'] and not channel.nsfw:
                    embed = None
                elif not isImage(post['url']):
                    embed = None
                else:
                    embed = discord.Embed(title=post['title'],
                                          color=discord.Color.orange(),
                                          url=f"https://www.reddit.com{post['permalink']}")
                    embed.set_image(url=post['url'])
                    embed.set_footer(
                        text=f"👍 {post['ups']} 💬 {post['num_comments']}")
            except KeyError as e:
                embed = None
            i += 1
            if i >= 5:
                raise commands.BadArgument(
                    f"Could not find a image from `{subreddit}`.")
        return embed

    class RedditView(ui.View):
        def __init__(self):
            super().__init__(timeout=120)

        async def interaction_check(self, interaction: discord.Interaction):
            return self.ctx.author == interaction.user

        @ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple)
        async def previous(self, button: ui.Button, interaction: discord.Interaction):
            if self.num > 0:
                self.num -= 1
                await interaction.message.edit(embed=self.log[self.num])
            else:
                await interaction.response.send_message("Cannot go to previous.", ephemeral=True)

        @ui.button(emoji='🛑', style=discord.ButtonStyle.red)
        async def on_stop(self, button: ui.Button, interaction: discord.Interaction):
            await self.ctx.tick()
            await interaction.message.edit(view=None)
            self.stop()

        @ui.button(emoji='➡️', style=discord.ButtonStyle.blurple)
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
        async def start(cls, ctx: ApolloContext):
            cls.ctx = ctx
            cls.log = []
            cls.num = 0
            embed = await post()
            cls.log.append(embed)
            await ctx.reply(embed=embed, view=cls())

    return RedditView
