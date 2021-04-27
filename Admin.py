import logging, random, sys, logging, discord, asyncio, secrets, subprocess, aiohttp, os
from io import BytesIO
from utils.mysql import *
from utils.channel_logger import Channel_Logger
from utils.tools import *
from utils.logger import log
from utils import checks, config
from utils.language import Language
from discord import ext
from random import randint, choice
from discord.ext import commands
from discord.ext.commands import Bot, bot_has_permissions, MissingPermissions, has_permissions

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(description="Pins the message with the specified ID to the channel")
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def pin(self, ctx, messageid:int):
		
		try:
			await ctx.message.delete()
			message = await ctx.channel.fetch_message(messageid)
		except discord.errors.NotFound:
			await ctx.send(Language.get("bot.no_message_found", ctx).format(messageid))
			return
		try:
			await message.pin()
			await ctx.send(f"Successfully pinned message with id {messageid}")
		except discord.errors.Forbidden:
			await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))
	@commands.command(description="Lists banned members")
	@commands.guild_only()
	async def getbans(self, ctx):
		
		# from utils import config
		x = await ctx.guild.bans()
		x = '\n'.join([str(y.user) for y in x])
		thing3 = "List of Banned Members\n" + x
		await ctx.send(thing3)
	@commands.command(usage="<user> <reason>", description="A nice ban command to use on rulebreakers.", brief="When you're just not having it")
	@has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *,  reason : str):
		
		guild = ctx.guild
		if member.id == config.owner_id:
			return await ctx.send("How dare you try to ban Pink!")	
		banembed=discord.Embed(title=f"{member} banned successfully", description=f"{member} banned for {reason}")
		dmembed = discord.Embed(title="Banned", description="You were banned from {} for {}".format(ctx.guild, reason))
		await ctx.send(embed=banembed)
		if not member.bot:
			await member.send(embed=dmembed)
		await member.ban(reason = reason)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=banembed)
	@commands.command(usage="<userid> <reason>", description="Ban ppl by id. Bot and user must have ban perms", aliases=["idban", "banbyid"])
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	@commands.guild_only()
	async def hackban(self, ctx, memberid : discord.Object, *, reason : str):
		guild = ctx.guild
		if not memberid:
			return await ctx.send("Provide an id pls")
		if memberid.id == config.owner_id:
			return await ctx.send("I'm not banning this person.")
		embed = discord.Embed(title=f"Successfully banned {memberid.id}", description=f"{memberid.id} banned for {reason}", color=0xff00f6)
		await ctx.send(embed=embed)
		await ctx.guild.ban(memberid, reason=reason)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
	@commands.command(name="kick", description="Kicks a user.", usage="<user> <reason>")
	@commands.guild_only()
	@commands.bot_has_permissions(kick_members=True)
	async def kick(self, ctx, member : discord.Member, *, reason : str):
		guild = ctx.guild
		if member.id in self.bot.owner_ids or member == ctx.author:
			return await ctx.send("I'm not kicking this person.")
		description = f"You've been a bad boy/girl, {member.mention}. You've been kicked."
		kickembed = discord.Embed(title="User kicked", description=description, color=0xf6d025, footer="Powered by: Terrabot")
		pmembed = discord.Embed(title="You've been kicked.", description=f"You've been kicked from {ctx.guild} for {reason}")
		await ctx.send(embed=kickembed)
		if not member.bot:
			await member.send(embed=pmembed)
		await member.kick(reason=reason)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=kickembed)
		logger.info(f"You've been bad, {member.mention}. You've been kicked.")
	@commands.command(name="addrole", description="Adds a role to a user")
	@commands.guild_only()
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	async def addrole(self, ctx, member: discord.Member, *, role:discord.Role):
		user=member
		if role is None:
			await ctx.send(Language.get("moderation.role_not_found", ctx).format(role))
			return
		name=role
		if role in member.roles:
			return await ctx.send("Cannot add this role to this user as they already have it! Nice try tho.")
		if role.position >= ctx.author.top_role.position:
			return await ctx.send("Nice try. You can't add a role that's higher than your own. Get an admin to do it")
		if role.position == ctx.me.top_role.position:
			return await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
		if role.position > ctx.me.top_role.position:
			return await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))

		await user.add_roles(role, reason=Language.get("moderation.addrole_reason", ctx).format(role, ctx.author))
		await ctx.send(Language.get("moderation.addrole_success", ctx).format(name, user))	
	@commands.command(usage="<userid>", description="Unbans a user")
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def unban(self, ctx, memberid : discord.Object):
		
		member = memberid
		try:
			await ctx.guild.unban(member)
			guild = ctx.guild
			description = f"Yay! {member.id} was unbanned"
			embed = discord.Embed(title="Member Unbanned", description=description)
			await ctx.send(embed=embed)
			for channel in guild.channels:
				if channel.name == "logs":
					await channel.send(embed=embed)
		except discord.errors.Forbidden:
			await ctx.send("I do not have the `Ban Members` permission.")
	
	@commands.command()
	@commands.guild_only()
	@commands.bot_has_permissions(manage_roles=True)
	@commands.has_permissions(manage_roles=True)
	async def removerole(self, ctx, member:discord.Member, *, rolename:discord.Role):
		"""Remove a role from someone."""
		guild = ctx.guild
		author = ctx.message.author
		await member.remove_roles(rolename, reason=None)
		embed=discord.Embed(title="Role removed", description="Role {} removed from {}".format(rolename, member), color=0xf6d025, footer="Powered by Terrabot")
		await ctx.send(embed=embed)
	@commands.command(aliases=["createrole", "rolecreate"])
	@commands.bot_has_permissions(manage_roles=True)
	@commands.has_permissions(manage_roles=True)
	@commands.guild_only()
	async def cr(self, ctx, *, rolename):
		"""Create a role"""
		r = randint(0, 0xFFFFFF)
		guild = ctx.guild
		author = ctx.message.author
		await guild.create_role(name="{}".format(rolename), colour = discord.Colour(r))
		embed = discord.Embed(title='New Role Created', color=0xf6d025)
		embed.add_field(name='Role:', value=rolename, inline=False)
		embed.add_field(name='Color:', value='#{}'.format(r), inline=False)
		embed.set_footer(text="Created by {}".format(ctx.message.author))
		await ctx.send(embed=embed)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
	

	@commands.command()
	@commands.guild_only()
	@has_permissions(ban_members=True)
	@bot_has_permissions(ban_members=True)
	async def massban(self, ctx, *, ids:str):
		"""Mass bans users by ids (separate ids with spaces)"""
		await ctx.channel.trigger_typing()
		ids = ids.split(" ")
		guild = ctx.guild
		failed_ids = []
		success = 0
		for id in ids:
			try:
				await self.bot.http.ban(int(id), ctx.guild.id, delete_message_days=0)
				success += 1
			except:
				failed_ids.append("`{}`".format(id))
		if len(failed_ids) != 0:
			await ctx.send(Language.get("moderation.massban_failed_ids", ctx).format(", ".join(ids)))
		await ctx.send(Language.get("moderation.massban_success", ctx).format(success, len(ids)))
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(Language.get("moderation.massban_success", ctx).format(success, len(ids)))
	@commands.guild_only()
	@commands.command()
	@bot_has_permissions(manage_roles=True)
	@has_permissions(manage_roles=True)
	async def renamerole(self, ctx, role:discord.Role, *, newname:str):
		"""Renames a role with the specified name, be sure to put double quotes (\") around the name and the new name"""
		if role is None:
			await ctx.send(Language.get("moderation.role_not_found", ctx).format(role))
			return
		try:
			await role.edit(reason=Language.get("moderation.renamerole_reason", ctx).format(ctx.author), name=newname)
			await ctx.send(Language.get("moderation.renamerole_success", ctx).format(role, newname))
		except discord.errors.Forbidden:
			if role.position == ctx.me.top_role.position:
				await ctx.send(Language.get("moderation.no_renamerole_highest_role", ctx))
			elif role.position > ctx.me.top_role.position:
				await ctx.send(Language.get("moderation.no_renamerole_higher_role", ctx))
			else:
				await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
	@commands.command()
	@commands.guild_only()
	@bot_has_permissions(manage_roles=True)
	@has_permissions(manage_roles=True)
	async def delrole(self, ctx, *, role:discord.Role):
		"""Delete a role. Must have manage roles perms"""
		guild = ctx.guild
		await role.delete()
		embed = discord.Embed(title="Role Deleted", description="Deleted the role {}".format(role.name), color=0xff00ae)
		embed.set_footer(text="Powered by Terrabot")
		await ctx.send(embed=embed)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
	
	@commands.command(usage="<name> <slomodetime>", description="create a text channel.")
	@commands.guild_only()
	@has_permissions(manage_channels=True)
	async def createtc(self, ctx, name, slowmodetime : int):
		
		guild = ctx.guild
		await ctx.guild.create_text_channel(name=name, slowmode_delay=slowmodetime)
		msg = discord.Embed(title="CHANNEL CREATED")
		msg.add_field(name= "Channel Name: ", value=name)
		msg.add_field(name= "Slowmode: ", value=slowmodetime)
		await ctx.send(embed=msg)
		for channel in guild.channels:
			if channel.name == "logs":	
				await channel.send(embed=msg)

	@commands.command(usage="<newname>", description="edit a text channel.")
	@commands.guild_only()
	@has_permissions(manage_channels=True)
	async def edittc(self, ctx, newname):
		topic = "This is a channel created by Terrabot"
		await ctx.channel.edit(name=newname, topic=topic)
		embed=discord.Embed(title="Renamed Channel Successfully", description=f"The channel has been renamed to {newname}")
		await ctx.send(embed=embed)

	@commands.command(help="Delete a text channel", usage="[channel]")
	@commands.guild_only()
	@commands.cooldown(1, 10,commands.BucketType.user)
	@commands.has_permissions(manage_channels=True)
	async def deletetc(self, ctx, channelname:discord.TextChannel):
		await channelname.delete()
		await ctx.send(f"Channel {channelname} was deleted by {ctx.author}")
		for channel in ctx.guild.channels:
			if channel.name == "logs":
				await channel.send(f"Channel {channelname} was deleted by {ctx.author}")

	@commands.command(aliases=['cs'], description="Sends a nice fancy embed with some channel stats")
	#@commands.bot_has_guild_permissions(manage_channels=True)
	async def channelstats(self, ctx):
		
		channel = ctx.channel
		embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=random.choice(self.bot.color_list))
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

		await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(Admin(bot))
