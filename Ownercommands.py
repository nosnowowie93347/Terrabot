import discord, aiohttp, sys, subprocess, logging, typing, traceback, json, os, requests, datetime, time, operator, math
from pathlib import Path
from discord.ext import commands
from utils.logger import log
import discord.utils
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions, bot_has_permissions
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
blacklisted_users = []
cwd = Path(__file__).parents[0]
cwd = str(cwd)
def setup(bot):
	bot.add_cog(Ownercommands(bot))
def read_json(filename):
	with open(f"{cwd}/bot_config/{filename}.json", "r") as file:
		data = json.load(file)
	return data
def write_json(data, filename):
	with open(f"{cwd}/bot_config/{filename}.json", "w") as file:
		json.dump(data, file, indent=4)

class Ownercommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	@commands.is_owner()
	async def unblacklist(self, ctx, user: discord.Member):
		blacklisted_users.remove(user.id)
		data = read_json("blacklist")
		data["blacklistedUsers"].remove(user.id)
		write_json(data, "blacklist")
		await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")
	@commands.command()
	@commands.is_owner()
	async def blacklist(self, ctx, user: discord.Member):
		if ctx.author.id == user.id:
			return await ctx.send("Hey! You can't blacklist yourself!")
		blacklisted_users.append(user.id)
		data = read_json("blacklist")
		data["blacklistedUsers"].append(user.id)
		write_json(data, "blacklist")
		await ctx.send(f"Hey, I've blacklisted {user.name} for you.")
	@commands.command(hidden=True)
	@commands.is_owner()
	@commands.cooldown(1, 7200, commands.BucketType.user)#only use every 2 hours
	async def rename(self, ctx, *, name:str):
		"""Renames the bot"""
		await self.bot.user.edit(username=name)
		await ctx.send(f"Hurray! My new name is {name}")
	@commands.command()
	@commands.is_owner()
	async def uploadfile(self, ctx, *, path:str):
		"""Uploads any file on the system. What is this hackery?"""
		await ctx.channel.trigger_typing()
		try:
			await ctx.send(file=discord.File(path))
		except FileNotFoundError:
			await ctx.send("That file does not exist!")
	@commands.command(hidden=True)
	@commands.is_owner()
	async def restart(self, ctx):
		"""Restarts the bot"""
		await ctx.send("Restarting...")
		log.warning("{} has restarted the bot!".format(ctx.author))
		try:
		  await aiosession.close()
		except:
		   pass
		await self.bot.logout()
		subprocess.call([sys.executable, "bot.py"])