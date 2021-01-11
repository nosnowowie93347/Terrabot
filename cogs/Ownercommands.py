import discord, aiohttp, sys, subprocess, logging, typing, traceback, json, os, requests, datetime, time, operator, math
from pathlib import Path
from discord.ext import commands
from utils.logger import log
import utils.json_loader
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
print(cwd)
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
			print(path)
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
	@commands.command(
		name="blacklist", description="Blacklist a user from the bot", usage="<user>"
	)
	@commands.is_owner()
	async def blacklist(self, ctx, user: discord.Member):
		if user.id in self.bot.owner_ids:
			await ctx.send("Cant blacklist an owner")
			return
		if user.id in self.bot.blacklisted_users:
			return await ctx.send("Cannot blacklist someone twice! :person_facepalming:")
		if ctx.message.author.id == user.id:
			await ctx.send("Hey, you cannot blacklist yourself!")
			return

		self.bot.blacklisted_users.append(user.id)
		data = utils.json_loader.read_json("blacklist")
		data["blacklistedUsers"].append(user.id)
		utils.json_loader.write_json(data, "blacklist")
		await ctx.send(f"Hey, I have blacklisted {user.name} for you.")
		print(self.bot.blacklisted_users)

	@commands.command(
		name="unblacklist",
		description="Unblacklist a user from the bot",
		usage="<user>",
	)
	@commands.is_owner()
	async def unblacklist(self, ctx, user: discord.Member):
		"""
		Unblacklist someone from the bot
		"""
		self.bot.blacklisted_users.remove(user.id)
		data = utils.json_loader.read_json("blacklist")
		data["blacklistedUsers"].remove(user.id)
		utils.json_loader.write_json(data, "blacklist")
		await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")
	@commands.command()
	async def get_blacklists(self, ctx):
		data = utils.json_loader.read_json("blacklist")
		await ctx.send(data)