import asyncio
import discord
from   discord.ext import commands

def setup(bot):
	# Add the bot and deps
	bot.add_cog(Face(bot))

# This is the Face module. It sends faces.

class Face(commands.Cog):

	# Init with the bot reference, and a reference to the settings var
	def __init__(self, bot):
		self.bot = bot

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

	
	