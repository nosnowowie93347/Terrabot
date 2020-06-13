import discord, random, asyncio, platform, time, os, datetime
from discord import ext
import re, copy, unicodedata
from collections import Counter
from discord.ext import commands
from discord.ext.commands import Bot


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
		for hours, 'm' for minutes and 's' for seconds. If no unit
		is given then it is assumed to be seconds. You can also combine
		multiple units together, e.g. 2h4m10s.
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

	
	@commands.command(aliases=["characterinfo"])
	async def charinfo(self, ctx, *, characters: str):
		"""Shows you information about a number of characters.
		Only up to 15 characters at a time.
		"""

		if len(characters) > 15:
			await ctx.send('Too many characters ({}/15)'.format(len(characters)))
			return

		def to_string(c):
			digit = format(ord(c), 'x')
			name = unicodedata.name(c, 'Name not found.')
			return '`0x{0}`: {1} - {2} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{0}>'.format(digit,
																											  name, c)

		await ctx.send('\n'.join(map(to_string, characters)))
	@commands.command(aliases=["botinvitelink", "invitebot"])
	async def join(self, ctx):
		"""Joins a server."""
		msg = 'It is no longer possible to ask me to join via invite. So use this URL instead.\n\n'
		perms = discord.Permissions.none()
		perms.read_messages = True
		perms.send_messages = True
		perms.manage_roles = True
		perms.ban_members = True
		perms.kick_members = True
		perms.manage_messages = True
		perms.embed_links = True
		perms.read_message_history = True
		perms.attach_files = True
		await ctx.send(msg + discord.utils.oauth_url("657372691749273612", perms))
	@commands.command()
	async def softban(self, ctx, member: discord.Object, *, reason: str):
		"""Soft bans a member from the server.
		A softban is basically banning the member from the server but
		then unbanning the member as well. This allows you to essentially
		kick the member while removing their messages.
		To use this command you must have Ban Members permissions or have
		the Bot Admin role. Note that the bot must have the permission as well.
		"""

		try:
			await ctx.guild.ban(member)
			await ctx.guild.unban(member, reason=reason)
		except discord.Forbidden:
			await ctx.send('The bot does not have permissions to ban members.')
		except discord.HTTPException:
			await ctx.send('Banning failed.')
		else:
			await ctx.send('\U0001f44c')


def setup(bot):
	bot.add_cog(YetAnotherCog(bot))