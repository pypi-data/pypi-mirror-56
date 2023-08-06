import asyncio
import pykeybasebot

class Command:
	def __init__(self, func, aliases=[], command_name=None):
		if not asyncio.iscoroutinefunction(func):
			raise TypeError('Callback must be a coroutine.')
		self.func = func

		self.command_name = command_name or func.__name__
		if not isinstance(self.command_name, str):
			raise TypeError('Name of a command must be a string.')

		self.invokable_by = [self.command_name, *aliases]
		if not isinstance(self.invokable_by, (list, tuple)):
			raise TypeError("'Invokable by' of a command must be a list of strings.")


class Context:
	def __init__(self, bot, event):
		self.bot = bot
		self.event = event

	async def send(self, message):
		await self.bot.bot.chat.send(self.event.msg.channel, str(message))
