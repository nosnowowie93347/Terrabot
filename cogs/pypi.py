import itertools, yaml, aiohttp
import logging
import random
import re

from discord import Embed
from discord.ext.commands import Cog, Context, command
from discord.utils import escape_markdown
with open("config-default.yml", encoding="UTF-8") as f:
	_CONFIG_YAML = yaml.safe_load(f)
class YAMLGetter(type):
	"""
	Implements a custom metaclass used for accessing
	configuration data by simply accessing class attributes.
	Supports getting configuration from up to two levels
	of nested configuration through `section` and `subsection`.
	`section` specifies the YAML configuration section (or "key")
	in which the configuration lives, and must be set.
	`subsection` is an optional attribute specifying the section
	within the section from which configuration should be loaded.
	Example Usage:
		# config.yml
		bot:
			prefixes:
				direct_message: ''
				guild: '!'
		# config.py
		class Prefixes(metaclass=YAMLGetter):
			section = "bot"
			subsection = "prefixes"
		# Usage in Python code
		from config import Prefixes
		def get_prefix(bot, message):
			if isinstance(message.channel, PrivateChannel):
				return Prefixes.direct_message
			return Prefixes.guild
	"""

	subsection = None

	def __getattr__(cls, name):
		name = name.lower()

		try:
			if cls.subsection is not None:
				return _CONFIG_YAML[cls.section][cls.subsection][name]
			return _CONFIG_YAML[cls.section][name]
		except KeyError:
			dotted_path = '.'.join(
				(cls.section, cls.subsection, name)
				if cls.subsection is not None else (cls.section, name)
			)
			log.critical(f"Tried accessing configuration variable at `{dotted_path}`, but it could not be found.")
			raise

	def __getitem__(cls, name):
		return cls.__getattr__(name)

	def __iter__(cls):
		"""Return generator of key: value pairs of current constants class' config values."""
		for name in cls.__annotations__:
			yield name, getattr(cls, name)
class RedirectOutput(metaclass=YAMLGetter):
	section = 'redirect_output'

	delete_delay: int
	delete_invocation: bool
class Colours(metaclass=YAMLGetter):
	section = "style"
	subsection = "colours"

	blue: int
	bright_green: int
	orange: int
	pink: int
	purple: int
	soft_green: int
	soft_orange: int
	soft_red: int
	white: int
	yellow: int
URL = "https://pypi.org/pypi/{package}/json"
PYPI_ICON = "https://cdn.discordapp.com/emojis/766274397257334814.png"
NEGATIVE_REPLIES = [
	"Noooooo!!",
	"Nope.",
	"I'm sorry Dave, I'm afraid I can't do that.",
	"I don't think so.",
	"Not gonna happen.",
	"Out of the question.",
	"Huh? No.",
	"Nah.",
	"Naw.",
	"Not likely.",
	"No way, José.",
	"Not in a million years.",
	"Fat chance.",
	"Certainly not.",
	"NEGATORY.",
	"Nuh-uh.",
	"Not in my house!",
]
PYPI_COLOURS = itertools.cycle((Colours.yellow, Colours.blue, Colours.white))

ILLEGAL_CHARACTERS = re.compile(r"[^-_.a-zA-Z0-9]+")
INVALID_INPUT_DELETE_DELAY = RedirectOutput.delete_delay

log = logging.getLogger(__name__)

class PyPi(Cog):
	"""Cog for getting information about PyPi packages."""

	def __init__(self, bot):
		self.bot = bot


	@command(name="pypi", aliases=("package", "pack"))
	async def get_package_info(self, ctx: Context, package: str) -> None:
		"""Provide information about a specific package from PyPI."""
		embed = Embed(title=random.choice(NEGATIVE_REPLIES), colour=Colours.soft_red)
		embed.set_thumbnail(url=PYPI_ICON)

		error = True

		if characters := re.search(ILLEGAL_CHARACTERS, package):
			embed.description = f"Illegal character(s) passed into command: '{escape_markdown(characters.group(0))}'"

		else:
			async with aiohttp.ClientSession() as session:
				async with session.get(URL.format(package=package)) as response:
					if response.status == 404:
						embed.description = "Package could not be found."

					elif response.status == 200 and response.content_type == "application/json":
						response_json = await response.json()
						info = response_json["info"]

						embed.title = f"{info['name']} v{info['version']}"

						embed.url = info["package_url"]
						embed.colour = next(PYPI_COLOURS)

						summary = escape_markdown(info["summary"])

						# Summary could be completely empty, or just whitespace.
						if summary and not summary.isspace():
							embed.description = summary
						else:
							embed.description = "No summary provided."

						error = False

					else:
						embed.description = "There was an error when fetching your PyPi package."
						log.trace(f"Error when fetching PyPi package: {response.status}.")

		if error:
			await ctx.send(embed=embed, delete_after=INVALID_INPUT_DELETE_DELAY)
			await ctx.message.delete(delay=INVALID_INPUT_DELETE_DELAY)
		else:
			await ctx.send(embed=embed)


def setup(bot):
	"""Load the PyPi cog."""
	bot.add_cog(PyPi(bot))