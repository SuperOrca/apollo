from discord.ext import commands
import discord
from discord import ui


class Context(commands.Context):
    async def reply(self, content: str = None, **kwargs):
        return await self.message.reply(content, **kwargs, mention_author=False)

    async def trash(self, content: str = None, **kwargs):
        class TrashView(ui.View):
            def __init__(self):
                super().__init__()

            @ui.button(label='🗑', style=discord.ButtonStyle.red)
            async def previous(self, button: ui.Button, interaction: discord.Interaction):
                if self.author == interaction.user:
                    await interaction.message.delete()
                else:
                    await interaction.response.send_message("This is not your command.", ephemeral=True)
        return await self.message.reply(content, **kwargs, mention_author=False, view=TrashView())
