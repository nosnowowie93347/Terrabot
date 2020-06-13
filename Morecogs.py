import asyncio
import discord
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import DisplayName
from   Cogs import Nullify

def setup(bot):
	# Add the bot and deps
	settings = bot.get_cog("Settings")
	bot.add_cog(Face(bot, settings))

# This is the Face module. It sends faces.

class Face(commands.Cog):

	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		global Utils, DisplayName
		Utils = self.bot.get_cog("Utils")
		DisplayName = self.bot.get_cog("DisplayName")

	@commands.command(pass_context=True)
	async def lenny(self, ctx, *, message : str = None):
		"""Give me some Lenny."""

		msg = "( ͡° ͜ʖ ͡°)"
		if message:
			msg += "\n{}".format(message)
		# Check for suppress
		
		# Send new message first, then delete original
		await ctx.send(msg)
		# Remove original message
		await ctx.message.delete()
		

	@commands.command(pass_context=True)
	async def shrug(self, ctx, *, message : str = None):
		"""Shrug it off."""

		msg = "¯\_(ツ)_/¯"
		if message:
			msg += "\n{}".format(message)
		# Send new message first, then delete original
		await ctx.send(msg)
		# Remove original message
		await ctx.message.delete()

	
	