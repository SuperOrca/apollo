from discord.ext import commands
import discord
from discord import ui
import asyncio


class TrashView(ui.View):
    def __init__(self, author):
        super().__init__(timeout=60)
        self.author = author

    @ui.button(emoji='🗑️', style=discord.ButtonStyle.red)
    async def delete(self, button: ui.Button, interaction: discord.Interaction):
        if self.author == interaction.user:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("This is not your command.", ephemeral=True)


class Context(commands.Context):
    async def reply(self, content: str = None, **kwargs):
        can_delete = kwargs.pop('can_delete', False)
        delete_after = kwargs.pop('delete_after', 0)
        if can_delete:
            msg = await self.message.reply(content, **kwargs, mention_author=False, view=TrashView(self.author))
        else:
            msg = await self.message.reply(content, **kwargs, mention_author=False)
        if delete_after > 0:
            await asyncio.sleep(delete_after)
            await msg.delete()
        return msg

    async def send(self, content: str = None, **kwargs):
        can_delete = kwargs.pop('can_delete', False)
        if can_delete:
            return await self.message.reply(
                content,
                **kwargs,
                mention_author=False,
                view=TrashView(self.author)
            )

        else:
            return await self.message.reply(content, **kwargs, mention_author=False)
