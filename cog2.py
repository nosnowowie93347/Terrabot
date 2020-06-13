import discord, random
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot
import platform, asyncio
class Other(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def revive(self, ctx):
		await ctx.send("Using my Holy Godlike powers to revive this here server...")
		await ctx.send(':thinking:')
		await asyncio.sleep(7)
		await ctx.send("Success!!")
	@commands.command()
	async def unrevive(self, ctx):
		await ctx.send("Why? Why would you kill a server?")
		await ctx.send("FINE")
		await asyncio.sleep(8)
		killoptions = ["Killed", "Kept the same. Command failed. HA THATS WHAT U GET FOR ATTEMPTED SERVER MURDER!"]
		await ctx.send("Your server has been " + random.choice(killoptions))
def setup(bot):
	bot.add_cog(Other(bot))