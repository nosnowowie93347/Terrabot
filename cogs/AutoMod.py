from asyncio import sleep
import re, logging, random, sys, discord, asyncio, secrets, subprocess, aiohttp, os
from datetime import datetime, timedelta
from re import search
from typing import Optional

from better_profanity import profanity
from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
	async def convert(self, ctx, argument):
		args = argument.lower()
		matches = re.findall(time_regex, args)
		time = 0
		for key, value in matches:
			try:
				time += time_dict[value] * float(key)
			except KeyError:
				raise commands.BadArgument(
					f"{value} is an invalid time key! h|m|s|d are valid arguments"
				)
			except ValueError:
				raise commands.BadArgument(f"{key} is not a number!")
		return round(time)

profanity.load_censor_words_from_file("./data/profanity.txt")

class AutoMod(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def mute_members(self, message, member:discord.Member, time: TimeConverter=None, *, reason):
		role = discord.utils.get(message.guild.roles, name="Muted")
		if not role:
			await message.channel.send("No muted role was found! Please create one called `Muted`")
			return

		try:
			if self.bot.muted_users[member.id]:
				await message.channel.send("This user is already muted")
				return
		except KeyError:
			pass

		data = {
			'_id': member.id,
			'mutedAt': datetime.now(),
			'muteDuration': time or None,
			'mutedBy': message.author.id,
			'guildId': message.guild.id,
		}
		await self.bot.mutes.upsert(data)
		self.bot.muted_users[member.id] = data

		await member.add_roles(role)

		if not time:
			await message.channel.send(f"Muted {member.display_name}")
		else:
			minutes, seconds = divmod(time, 60)
			hours, minutes = divmod(minutes, 60)
			if int(hours):
				await message.channel.send(
					f"Muted {member.display_name} for {hours} hours, {minutes} minutes and {seconds} seconds"
				)
			elif int(minutes):
				await message.channel.send(
					f"Muted {member.display_name} for {minutes} minutes and {seconds} seconds"
				)
			elif int(seconds):
				await message.channel.send(f"Muted {member.display_name} for {seconds} seconds")

	async def unmute_members(self, guild, member:discord.Member, *, reason="Mute time expired."):
		role2 = discord.utils.get(guild.roles, name="Muted")
		await member.remove_roles(role2)
		

		await self.bot.mutes.delete(member.id)
		embed = Embed(title="Member unmuted",
			colour=0xDD2222,
			timestamp=datetime.utcnow())

		embed.set_thumbnail(url=member.avatar_url)

		fields = [("Member", member.display_name, False),
				  ("Reason", reason, False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		logchannel = discord.utils.get(member.guild.text_channels, name="moderator-log")
		await self.log_channel.send(embed=embed)
		try:
			self.bot.muted_users.pop(member.id)
		except KeyError:
			pass

	@command(name="addprofanity", aliases=["addswears", "addcurses"])
	@has_permissions(manage_guild=True)
	async def add_profanity(self, ctx, *words):
		with open("./data/profanity.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.send("Action complete.")

	@command(name="delprofanity", aliases=["delswears", "delcurses"])
	@has_permissions(manage_guild=True)
	async def remove_profanity(self, ctx, *words):
		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]

		with open("./data/profanity.txt", "w", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.send("Action complete.")
	@Cog.listener()
	async def on_ready(self):
		self.log_channel = self.bot.get_channel(832961664433389568)
	@Cog.listener()
	async def on_message(self, message):
		

		if not message.author.bot:
			if profanity.contains_profanity(message.content):
				await message.delete()
				await message.channel.send("You can't use that word here.", delete_after=10)
				unmutes = await self.mute_members(message, message.author, None, reason="Blacklisted word")

				
				await sleep(60)
				await self.unmute_members(message.guild, message.author)
def setup(bot):
	bot.add_cog(AutoMod(bot))