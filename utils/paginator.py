from typing import List, Optional
import itertools


from discord import ui
import discord


from utils.metrics import Embed
from utils.context import ApolloContext


class EmbedPaginator(ui.View):
    page = 0

    async def interaction_check(self, interaction: discord.Interaction):
        if not self.ctx.author == interaction.user:
            await interaction.response.send_message(
                f"This view is owned by {self.ctx.author.mention}. You make your own view by using the `{self.ctx.command}` command.",
                ephemeral=True)
            return False
        return True

    @ui.button(emoji='⏮', style=discord.ButtonStyle.secondary)
    async def on_start(self, button: ui.Button, interaction: discord.Interaction):
        if self.page != self.first_page:
            self.page = self.first_page
            await interaction.message.edit(embed=self.embeds[self.page])

    @ui.button(emoji='◀', style=discord.ButtonStyle.secondary)
    async def on_back(self, button: ui.Button, interaction: discord.Interaction):
        if self.page > self.first_page:
            self.page -= 1
            await interaction.message.edit(embed=self.embeds[self.page])

    @ui.button(emoji='⏹️', style=discord.ButtonStyle.secondary)
    async def on_stop(self, button: ui.Button, interaction: discord.Interaction):
        await self.ctx.tick()
        self.stop()
        await interaction.message.delete()

    @ui.button(emoji='▶', style=discord.ButtonStyle.secondary)
    async def on_forward(self, button: ui.Button, interaction: discord.Interaction):
        if self.page < self.last_page:
            self.page += 1
            await interaction.message.edit(embed=self.embeds[self.page])

    @ui.button(emoji='⏭', style=discord.ButtonStyle.secondary)
    async def on_end(self, button: ui.Button, interaction: discord.Interaction):
        if self.page != self.last_page:
            self.page = self.last_page
            await interaction.message.edit(embed=self.embeds[self.page])

    @classmethod
    async def start(cls, ctx: ApolloContext, embeds: List[Embed], timeout: Optional[float] = 180):
        cls.ctx = ctx
        cls.embeds = embeds
        cls.last_page = len(embeds) - 1
        cls.first_page = 0
        await ctx.reply(embed=embeds[cls.first_page], view=cls(timeout=timeout))
