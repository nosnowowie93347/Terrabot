import discord, random, asyncio, platform, time, os, datetime, aiohttp
from discord import ext
import re, copy, unicodedata
from collections import Counter
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, bot_has_permissions
from utils2.EmojiStealer import *

class TimeParser:
	def __init__(self, argument):
		compiled = re.compile(r"(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?")  
		self.original = argument
		try:
			self.seconds = int(argument)
		except ValueError as e:
			match = compiled.match(argument)
			if match is None or not match.group(0):
				raise commands.BadArgument('Failed to parse time.') from e
			self.seconds = 0
			hours = match.group('hours')
			if hours is not None:
				self.seconds += int(hours) * 3600
			minutes = match.group('minutes')
			if minutes is not None:
				self.seconds += int(minutes) * 60
			seconds = match.group('seconds')
			if seconds is not None:
				self.seconds += int(seconds)

		if self.seconds < 0:
			raise commands.BadArgument('I don\'t do negative time.')

		if self.seconds > 604800:  # 7 days
			raise commands.BadArgument('That\'s a bit too far in the future for me.')

class YetAnotherCog(commands.Cog):
	def __init___(self,bot):
		self.bot = bot

	@commands.command()
	async def timer(self, ctx, time: TimeParser, *, message=''):
		"""Reminds you of something after a certain amount of time.
		 The time can optionally be specified with units such as 'h'
		for hours, 'm' for minutesand 's' for seconds.
		"""

		author = ctx.message.author
		reminder = None
		completed = None
		message = message.replace('@everyone', '@\u200beveryone')

		if not message:
			reminder = 'Okay {0.mention}, I\'ll remind you in {1.seconds} seconds.'
			completed = 'Time is up {0.mention}! You asked to be reminded about something.'
		else:
			reminder = 'Okay {0.mention}, I\'ll remind you about "{2}" in {1.seconds} seconds.'
			completed = 'Time is up {0.mention}! You asked to be reminded about "{1}".'

		await ctx.send(reminder.format(author, time, message))
		await asyncio.sleep(time.seconds)
		await ctx.send(completed.format(author, message))
	@commands.command(usage="<userid> <reason>")
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def softban(self, ctx, member: discord.User, *, reason: str):
		"""Soft bans a member from the server.
		A softban is basically banning the member from the server but
		then unbanning the member as well. This allows you to essentially
		kick the member while removing their messages.
		"""
		try:
			guild = ctx.guild
			await member.send(f"You've been softbanned in {guild} by {ctx.message.author} for {reason}")
			await ctx.guild.ban(member)
			await ctx.guild.unban(member, reason=reason)
		except discord.Forbidden:
			await ctx.send('The bot does not have permissions to ban members.')
		except discord.HTTPException:
			await ctx.send('Banning failed.')
		else:
			await ctx.send('\U0001f44c {} banned successfully.'.format(member))
	
	@commands.command()
	@commands.has_permissions(manage_emojis=True)
	@commands.bot_has_permissions(manage_emojis=True)
	async def steal_emoji(self, ctx, emoji: EmojiThief, name=None):
		"""Steals an emoji from another server. Args are ID and name."""
		# the converter can return none when cancelled.
		if not emoji:
			return

		extension = "gif" if emoji.animated else "png"
		emoji_url = f"https://cdn.discordapp.com/emojis/{emoji.id}.{extension}"

		if not emoji.name and not name:
			await ctx.send(
				"The name of the emoji could not be resolved. Please specify one."
			)
			return

		name = emoji.name or name.strip(":")
		msg = await ctx.send("<:loading:725036771741663272>")

		try:
			async with aiohttp.ClientSession() as se:
				async with se.get(emoji_url, raise_for_status=True) as resp:
					data = await resp.read()
					emoji = await ctx.guild.create_custom_emoji(name=name, image=data)

					try:
						await msg.edit(content=str(emoji))
						await msg.add_reaction(emoji)
					except discord.HTTPException as fuck:
						await ctx.send(fuck)
		except aiohttp.ClientError:
			await msg.edit(content="Failed to download the emoji.")
		except discord.HTTPException as exc:
			await msg.edit(content=f"Failed to upload the emoji: {exc}")

def setup(bot):
	bot.add_cog(YetAnotherCog(bot))