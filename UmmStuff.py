import discord, sys, os, random, pathlib
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, bot_has_permissions

class UmmStuff(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	@commands.command(name="upgradedpurge",aliases=['p'], pass_context=True, no_pm=True)
	@commands.bot_has_permissions(manage_messages=True)
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def betterpurgecommand(self, ctx, msgs: int, members="everyone", *, txt=None):
		"""Purge last n messages or nmessages with a word. Requires Manage Messages permission. [p]help purge for more info.
		
		Ex:
		
		[p]purge 20 - deletes the last 20 messages in a channel sent by anyone.
		[p]purge 20 everyone stuff - deletes any messages in the last 20 messages that contain the word 'stuff'.
		[p]purge 20 @appu1232 - deletes any messages in the last 20 messages that were sent by appu1232.
		[p]purge 20 "@appu1232, LyricLy, 435254873976547426" hello - deletes any messages in the last 20 messages that were sent by appu1232, LyricLy or thecommondude that contain the word 'stuff'.
		"""
		await ctx.message.delete()
		member_object_list = []
		if members != "everyone":
			member_list = [x.strip() for x in members.split(",")]
			for member in member_list:
				if "@" in member:
					member = member[3 if "!" in member else 2:-1]
				if member.isdigit():
					member_object = ctx.guild.get_member(int(member))
				else:
					member_object = ctx.guild.get_member_named(member)
				if not member_object:
					return await ctx.send("Invalid user.")
				else:
					member_object_list.append(member_object)

		if msgs < 10000:
			async for message in ctx.message.channel.history(limit=msgs):
				try:
					if txt:
						if not txt.lower() in message.content.lower():
							continue
					if member_object_list:
						if not message.author in member_object_list:
							continue

					await message.delete()
				except discord.Forbidden:
					await ctx.send("You do not have permission to delete other users' messages. Use t%wipe instead to delete your own messages.")
		else:
			await ctx.send('Too many messages to delete. Enter a number < 10000')
def setup(bot):
	bot.add_cog(UmmStuff(bot))