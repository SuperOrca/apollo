import discord
from discord import ui
from discord.ext import commands


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


class ApolloContext(commands.Context):
    async def reply(self, content: str = None, **kwargs):
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

    async def send(self, content: str = None, **kwargs):
        can_delete = kwargs.pop('can_delete', False)
        if can_delete:
            return await self.channel.send(
                content,
                **kwargs,
                view=TrashView(self.author)
            )

        else:
            return await self.channel.send(content, **kwargs)
