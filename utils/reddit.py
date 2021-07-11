import random

import discord
from discord.ext import commands, menus
from discord import ui

from .metrics import isImage
from .views import ViewMenu


async def getpost(bot, channel, subreddit) -> discord.Embed:
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
            if i >= 3:
                raise commands.BadArgument(
                    f"Could not find a image from `{subreddit}`.")
        return embed

    class RedditMenu(ui.View):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.timeout = 180

        @ui.button(label='⬅️', style=discord.ButtonStyle.blurple)
        async def previous(self, button: ui.Button, interaction: discord.Interaction):
            if self.ctx.author.id == interaction.user.id:
                if self.num > 0:
                    self.num -= 1
                    await self.message.edit(embed=self.log[self.num], view=self.build())
                else:
                    await interaction.response.send_message("Cannot go to previous.", ephemeral=True)
            else:
                await interaction.response.send_message("This is not your command.", ephemeral=True)

        @ui.button(label='🛑', style=discord.ButtonStyle.red)
        async def on_stop(self, button: ui.Button, interaction: discord.Interaction):
            if self.ctx.author.id == interaction.user.id:
                await self.message.edit(view=None)
            else:
                await interaction.response.send_message("This is not your command.", ephemeral=True)

        @ui.button(label='➡️', style=discord.ButtonStyle.blurple)
        async def forwards(self, button: ui.Button, interaction: discord.Interaction):
            if self.ctx.author.id == interaction.user.id:
                self.num += 1
                try:
                    await self.message.edit(embed=self.log[self.num], view=self.build())
                except IndexError:
                    embed = await post()
                    self.log.append(embed)
                    await self.message.edit(embed=embed, view=self.build())
            else:
                await interaction.response.send_message("This is not your command.", ephemeral=True)

        async def start(self, ctx: commands.Context):
            self.ctx = ctx
            self.log = []
            self.num = 0
            embed = await post()
            self.log.append(embed)
            self.message = await ctx.reply(embed=embed, view=self.build())

        def build(self):
            return self()

    return RedditMenu
