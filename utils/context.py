import discord
from discord import ui
from discord.ext import commands


class TrashView(ui.View):
	def __init__(self, ctx):
		super().__init__(timeout=180)
		self.ctx = ctx

	async def interaction_check(self, interaction: discord.Interaction):
		if not self.ctx.author == interaction.user:
			await interaction.response.send_message(f"This view is owned by {self.ctx.author.mention}. You make your own view by using the `{self.ctx.command}` command.", ephemeral=True)
			return False
		return True

	@ui.button(emoji='🗑️', style=discord.ButtonStyle.red)
	async def delete(self, button: ui.Button, interaction: discord.Interaction):
		await self.ctx.tick()
		self.stop()
		await interaction.message.delete()


class ApolloContext(commands.Context):
	async def reply(self, content: str = None, **kwargs) -> discord.Message:
		"""Adds a can_delete kwarg to the reply method."""
		can_delete = kwargs.pop('can_delete', False)
		if can_delete:
			return await self.message.reply(
				content,
				**kwargs,
				mention_author=False,
				view=TrashView(self)
			)

		else:
			return await self.message.reply(content, **kwargs, mention_author=False)

	async def send(self, content: str = None, **kwargs) -> discord.Message:
		"""Adds a can_delete kwarg to the send method."""
		can_delete = kwargs.pop('can_delete', False)
		if can_delete:
			return await self.channel.send(
				content,
				**kwargs,
				view=TrashView(self)
			)
		else:
			return await self.channel.send(content, **kwargs)

	async def tick(self, tick: bool = True) -> None:
		"""Adds a tick method to the context."""
		try:
			if tick:
				await self.message.add_reaction('<:greenTick:596576670815879169>')
			elif tick is None:
				await self.message.add_reaction('<:grayTick:596576672900186113>')
			else:
				await self.message.add_reaction('<:redTick:596576672149667840>')
		except:
			...
