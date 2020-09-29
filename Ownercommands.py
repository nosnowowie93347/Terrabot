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

class Ownercommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(hidden=True)
	@commands.is_owner()
	@commands.cooldown(1, 7200, commands.BucketType.user)#only use every 2 hours
	async def rename(self, ctx, *, name:str):
		"""Renames the bot"""
		await self.bot.user.edit(username=name)
		await ctx.send(f"Hurray! My new name is {name}")
	@commands.command(aliases=["attachfile"])
	@commands.is_owner()
	async def uploadfile(self, ctx, *, path:str):
		"""Uploads any file on the system. What is this hackery?"""
		await ctx.channel.trigger_typing()
		try:
			await ctx.send(file=discord.File(path))
		except FileNotFoundError:
			await ctx.send("That file does not exist!")
	@commands.command(hidden=False)
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
	@commands.command(usage="<channel>")
	@commands.is_owner()
	async def lockdown(self, ctx, channel: discord.TextChannel = None):
		channel = channel or ctx.channel
		if ctx.guild.default_role not in channel.overwrites:
			# This is the same as the elif except it handles agaisnt empty overwrites dicts
			overwrites = {
				ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
			}
			await channel.edit(overwrites=overwrites)
			await ctx.send(f"I have put {channel.name} on lockdown.")
		elif (
			channel.overwrites[ctx.guild.default_role].send_messages == True
			or channel.overwrites[ctx.guild.default_role].send_messages == None
		):
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send(f"I have put {channel.name} on lockdown.")
		else:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = True
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send(f"I have removed {channel.name} from lockdown.")