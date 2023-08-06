from .models import Command, Context
import pykeybasebot
import asyncio

class Bot:
	def __init__(self, prefix: str, username: str, paperkey:str=None):
		# Arguments
		self.prefix = prefix
		self.username = username
		self.paperkey = paperkey
		self.bot = pykeybasebot.Bot(username=self.username, paperkey=self.paperkey, handler=self._pykeybasebot_handler)

		self.commands = []

	def command(self, aliases=[], command_name=None):
		def wrap(func):
			def wrapped_func(*args, **kwargs):
				return func(*args, **kwargs)
			self.commands.append(Command(func, aliases, command_name))
			return wrapped_func
		return wrap

	async def _pykeybasebot_handler(self, bot, event):
		if event.type == pykeybasebot.EventType.CHAT and event.source == pykeybasebot.Source.REMOTE:
			if event.msg.content.type_name == "text":
				text = event.msg.content.text.body.strip()
				if text.startswith(self.prefix):
					args = text.replace("!", "", 1).split(" ")

					for command in self.commands:
						if args[0] in command.invokable_by:
							return await command.func(Context(self, event), *args[1:])

	def run(self):
		listen_options = {
    		"local": True,
    		"wallet": True,
    		"dev": True,
    		"hide-exploding": False,
    		"filter_channel": None,
    		"filter_channels": None,
		}

		asyncio.run(self.bot.start(listen_options))
