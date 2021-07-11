from discord.ext import commands
import discord


class Context(commands.Context):
    @discord.utils.copy_doc(discord.Message.reply)
    async def reply(self, content: str = None, **kwargs):
        return await self.message.reply(content, **kwargs, mention_author=False)