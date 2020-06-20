import discord, platform, requests, json, random, fnmatch, time, asyncio, os, datetime
from discord import ext
from   Cogs import ReadableTime
from discord.ext import commands
from utils.language import Language
from utils.mysql import *
from utils.channel_logger import Channel_Logger
from utils.tools import *
from utils import checks
from discord.ext.commands import Bot, has_permissions, MissingPermissions

bot_status = discord.Status.online
class Botstuff(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.startTime = int(time.time())
	
	@commands.command()
	async def cloc(self, ctx):
		import os
		"""Outputs the total count of lines of code in the currently installed repo."""
		# Script pulled and edited from https://github.com/kyco/python-count-lines-of-code/blob/python3/cloc.py
		
		# Get our current working directory - should be the bot's home
		path = os.getcwd()
		
		# Set up some lists
		extensions = []
		code_count = []
		include = ['py',"bat", 'sh','command']
		
		# Get the extensions - include our include list
		extensions = self.get_extensions(path, include)
		
		for run in extensions:
			extension = "*."+run
			temp = 0
			for root, dir, files in os.walk(path):
				for items in fnmatch.filter(files, extension):
					value = root + "/" + items
					temp += sum(+1 for line in open(value, 'rb'))
			code_count.append(temp)
			pass
		
		# Set up our output
		msg = 'Some poor soul took the time to sloppily write the following to bring me life:\n```\n'
		padTo = 0
		for idx, val in enumerate(code_count):
			# Find out which has the longest
			tempLen = len(str('{:,}'.format(code_count[idx])))
			if tempLen > padTo:
				padTo = tempLen
		for idx, val in enumerate(code_count):
			lineWord = 'lines'
			if code_count[idx] == 1:
				lineWord = 'line'
			# Setup a right-justified string padded with spaces
			numString = str('{:,}'.format(code_count[idx])).rjust(padTo, ' ')
			msg += numString + " " + lineWord + " of " + extensions[idx] + "\n"
			# msg += extensions[idx] + ": " + str(code_count[idx]) + ' ' + lineWord + '\n'
			# print(extensions[idx] + ": " + str(code_count[idx]))
			pass
		msg += '```'
		await ctx.send(msg)
		
	def get_extensions(self, path, excl):
		extensions = []
		for root, dir, files in os.walk(path):
			for items in fnmatch.filter(files, "*"):
				temp_extensions = items.rfind(".")
				ext = items[temp_extensions+1:]
				if ext not in extensions:
					if ext in excl:
						extensions.append(ext)
						pass
		return extensions
	@commands.command(aliases=["botinfo"])
	async def about(self, ctx):
		"""About the Bot"""
		embed = discord.Embed(color=0x676767)
		embed.set_author(name="Terrabot", icon_url="https://cdn.discordapp.com/avatars/657372691749273612/67d2caa88aad928296c23b2aa964384d.webp?size=1024")
		embed.set_footer(text="Terrabot | Created by Pinkalicious21902")
		embed.add_field(name="What is Terrabot?", value="Terrabot is a general purpose bot built on the discord.py library. The bot began as a fun project and will continue to have updates pushed out as I learn more.")
		embed.add_field(name="Need help on how to use it?", value="You can check the help command by doing \n\n``%help`` \n\n Updates will constantly be pushed out with more features and new commands.")

		await ctx.send(embed=embed)
	@commands.command()
	async def futurecommands(self, ctx):
		"""Coming Soon"""
		comingsoon = "More commands coming soon!"
		await ctx.send(comingsoon)
	@commands.command()
	async def uptime(self, ctx):
		"""Lists the bot's uptime."""
		currentTime = int(time.time())
		timeString  = ReadableTime.getReadableTimeBetween(self.startTime, currentTime)
		msg = 'I\'ve been up for *{}*.'.format(timeString)
		await ctx.send(msg)
	@commands.command(name="platform")
	async def platforms(self, ctx):
		"""Tells the platform the bot's running on"""
		await ctx.send("The bot is currently running on: ```" + str(platform.platform()) + "```")
	@commands.command(aliases=["listofservers", "sl"])
	async def serverlist(self, ctx):
		"""Lists the servers Terrabot is in"""
		x = ', '.join([str(server) for server in self.bot.guilds])
		y = len(self.bot.guilds)
		print("Server list: " + x)
		if y > 40:
			thing = "Currently active on " + str(y) + " servers:", "fuck" + "```json\nCan't display more than 40 servers!```"
			await ctx.send(thing)
		elif y < 40:
			thing2 = "Currently active on " + str(y) + " servers:" + "```json\n" + x + "```"
			await ctx.send(thing2)
	@commands.command(aliases=["checklatency", "botping", "serverping"])
	async def ping(self, ctx):
		"""Gets bot latency"""
		print(self.bot.latency)
		before_typing = time.monotonic()
		await ctx.trigger_typing()
		after_typing = time.monotonic()
		ms = int((after_typing - before_typing) * 1000)
		msg = '*{}*, ***PONGY PONG!*** :ping_pong:'.format(ctx.author.mention)
		msg2 = ':hourglass: (~{}ms)'.format(ms)
		await ctx.send(msg)
		await ctx.send(msg2)
	@commands.command()
	async def idlebot(self, ctx):
		"""Idles the bot"""
		await self.bot.change_presence(activity=None, status=discord.Status.idle)
	@commands.command(hidden=True)
	async def donotdisturb(self, ctx):
		'''sets bot status to DND'''
		await self.bot.change_presence(activity=None, status=discord.Status.dnd)
		await ctx.send('Successfully changed bot status')
	@commands.command(aliases=["killme", "logout"])
	@commands.is_owner()
	async def shutdown(self, ctx):
		"""Shuts down the bot."""
		await ctx.send("logging out...")
		await self.bot.logout()
	@commands.command(aliases=["changestatus", "changeactivity"])
	@has_permissions(change_nickname=True)
	async def change_status(self, ctx, *, message):
		"""Changes the bot's status"""
		playingrn = message
		await self.bot.change_presence(activity=discord.Game(name=playingrn), status=bot_status)
		await ctx.send(f"Success! Status changed to {playingrn}")
	@commands.command()
	
	async def unpin(self, ctx, id:int):
		"""Unpins the message with the specified ID from the channel"""
		pinned_messages = await ctx.channel.pins()
		message = discord.utils.get(pinned_messages, id=id)
		if message is None:
			await ctx.send(Language.get("moderation.no_pinned_message_found", ctx).format(id))
			return
		try:
			await message.unpin()
			await ctx.send(Language.get("moderation.unpin_success", ctx))
		except discord.errors.Forbidden:
			await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))
	@commands.command(hidden=True)
	async def listwarns(self, ctx):
		role = discord.utils.get(ctx.guild.roles, name='Warned')
		warnList = role.members

		if not len(warnList):
			await ctx.send("No one is currently Warned.")
			return

		# We have at least one member warned
		msg = 'Currently Warned:\n\n'
		msg += ', '.join([member.name for member in warnList])

		await ctx.send(msg)
def setup(bot):
	bot.add_cog(Botstuff(bot))