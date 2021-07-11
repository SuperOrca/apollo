import random

import discord
from discord.ext import commands
from discord.ext import menus

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

    class PostMenu(ViewMenu):
        def __init__(self):
            super().__init__(clear_reactions_after=True)
            self.message = None
            self.timeout = 180
            self.log = []
            self.num = 0

        async def send_initial_message(self, ctx, channel):
            embed = await post()
            self.log.append(embed)
            self.message = await self.send_with_view(channel, embed=embed)
            return self.message

        @menus.button("⬅️")
        async def back(self, interaction):
            if self.ctx.author.id == interaction.user.id:
                if self.num > 0:
                    self.num -= 1
                    await self.message.edit(embed=self.log[self.num])

        @menus.button("➡️")
        async def forward(self, interaction):
            if self.ctx.author.id == interaction.user.id:
                self.num += 1
                try:
                    await self.message.edit(embed=self.log[self.num])
                except IndexError:
                    embed = await post()
                    self.log.append(embed)
                    await self.message.edit(embed=embed)

        @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
        async def on_stop(self, interaction):
            if self.ctx.author.id == interaction.user.id:
                self.stop()

        async def start(self, ctx):
            await super().start(ctx)
            self.ctx = ctx

    return PostMenu()
