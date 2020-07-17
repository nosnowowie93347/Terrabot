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
	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def pin(self, ctx, messageid:int):
		"""Pins the message with the specified ID to the channel"""
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
	@commands.command()
	async def getbans(self, ctx):
		"""Lists banned members"""
		from utils import config
		x = await ctx.guild.bans()
		x = '\n'.join([str(y.user) for y in x])
		thing3 = "List of Banned Members\n" + x
		await ctx.send(thing3)
	@commands.command()
	@has_permissions(ban_members=True)
	@commands.bot_has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *,  reason : str):
		"""When you're just not having it"""
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
	@commands.command(aliases=["idban", "banbyid"])
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def hackban(self, ctx, memberid : discord.Object, *, reason : str):
		"""Ban ppl by id. Bot and user must have ban perms"""
		guild = ctx.guild
		if memberid.id == config.owner_id:
			return await ctx.send("I'm not banning this person.")
		embed = discord.Embed(title=f"Successfully banned {memberid.id}", description=f"{memberid.id} banned for {reason}", color=0xff00f6)
		await ctx.send(embed=embed)
		await ctx.guild.ban(memberid, reason=reason)
		await ctx.message.delete()
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
	@commands.command(name="kick")
	async def kick(self, ctx, member : discord.Member, *, reason : str):
		"""Kicks a user."""
		guild = ctx.guild
		if member.id == config.owner_id or member == ctx.author:
			return await ctx.send("I'm not kicking this person.")
		description = f"You've been bad, {member.mention}. You've been kicked."
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
	@commands.command(name="addrole")
	@commands.guild_only()
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	async def addrole(self, ctx, member: discord.Member, *, role:discord.Role):
		"""Adds a role to a user"""
		user=member
		if role is None:
			await ctx.send(Language.get("moderation.role_not_found", ctx).format(role))
			return
		name=role
		await user.add_roles(role, reason=Language.get("moderation.addrole_reason", ctx).format(role, ctx.author))
		await ctx.send(Language.get("moderation.addrole_success", ctx).format(name, user))	
	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, memberid : discord.Object):
		"""Unbans a user"""
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
	@commands.command(name='mute')
	@has_permissions(manage_roles=True)
	@bot_has_permissions(manage_roles=True)
	async def mute_cmd(self, ctx, member: discord.Member, *, reason:str):
		"""Mute ppl who break the rules"""
		guild = ctx.guild
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		if not role:
			return await ctx.send(f'Unable to Mute {ctx.author} - No Role was Found')
		if role in member.roles:
			return await ctx.send(f'Unable to Mute {ctx.author} - User Already Muted')
		if member is ctx.author:
			msg = 'It would be easier for me if you just *stayed quiet all by yourself...*'
			return await ctx.send(msg)
		#check if bot owner is muted
		if member.id == 466778567905116170:
			return await ctx.send("... I can't betray my master!!")

		# Check if we're muting the bot
		if member.id == self.bot.user.id:
			msg = 'How about we don\'t, and *pretend* we did...'
			return await ctx.send(msg)
		try:
			await member.add_roles(role)

			embed = discord.Embed(title = 'User Muted',color = 0xff00f6,description = f'{member.mention} was muted by {ctx.author.mention}')
			mutedmembed = discord.Embed(title="You've been muted.", color=0xff00f6, description=f"You've been muted in {guild} by {ctx.author} for {reason}.")
			await ctx.send(embed=embed)
			if not member.bot:
				await member.send(embed=mutedmembed)
			for channel in guild.channels:
				if channel.name == "logs":
					await channel.send(embed=embed)
			logger.info("Muted {} for {}".format(member, reason))
		except discord.errors.Forbidden:
			if role.position == ctx.me.top_role.position:
				await ctx.send("I cannot add the mute role to users as it's my highest role")
			elif mute_role.position > ctx.me.top_role.position:
				await ctx.send("I cannot add the mute role to users as it's higher than my highest role.")
			else:
				await ctx.send("I do not have the `Manage Roles` permission.")
	@commands.command(name="unmute")
	@has_permissions(manage_roles=True)
	async def unmute_command(self, ctx, member : discord.Member):
		"""Unmute. Just in case."""
		guild = ctx.guild
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		if not role:
			await ctx.send("User not muted")
			return await ctx.send(f"Unable to unmute {ctx.author} - No role found")
		if role in member.roles:
			await member.remove_roles(role)
			embed = discord.Embed(title= "User Unmuted", color=0xff00f6,description= f'{member.mention} was unmuted by {ctx.author.mention}')
			await ctx.send(embed=embed)
			if not member.bot:
				await member.send(f"You were unmuted by {ctx.author} in {ctx.guild}.")
			for channel in guild.channels:
				if channel.name == "logs":
					await channel.send(embed=embed)
	@commands.command()
	@bot_has_permissions(manage_roles=True)
	@has_permissions(manage_roles=True)
	async def unwarn(self, ctx, member:discord.Member=None, *, reason:str):
		"""If for whatever reason you want to unwarn someone"""
		embed=discord.Embed(title="Unwarned User", description="Unwarned {} for {}".format(member, reason))
		role = discord.utils.get(ctx.guild.roles, name="Warned")
		await member.remove_roles(role)
		await ctx.send(embed=embed)
		if not member.bot:
			await member.send(f"You were unwarned in {ctx.guild}.")
	@commands.command()
	@bot_has_permissions(manage_roles=True)
	async def warn(self, ctx, member:discord.Member, *, reason:str):
		"""Warn Someone."""
		guild = ctx.guild
		embed = discord.Embed(title="Warned User", color=0xff00f6,description=f'{member.mention} was warned by {ctx.author.mention}')
		role = discord.utils.get(ctx.guild.roles, name='Warned')
		if role not in guild.roles:
			await guild.create_role(name="Warned", hoist=True)
		await member.add_roles(role)
		await ctx.send(embed=embed)
		if not member.bot:
			await member.send(embed=embed)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
		logger.info("Warned {} for {}".format(member, reason))
	@commands.command()
	@commands.bot_has_permissions(manage_roles=True)
	@commands.has_permissions(manage_roles=True)
	async def removerole(self, ctx, member:discord.Member, *, rolename:discord.Role):
		"""Remove a role from someone. Must have manage role perms"""
		guild = ctx.guild
		author = ctx.message.author
		await member.remove_roles(rolename, reason=None)
		embed=discord.Embed(title="Role removed", description="Role {} removed from {}".format(rolename, member), color=0xf6d025, footer="Powered by Terrabot")
		await ctx.send(embed=embed)
	@commands.command(aliases=["createrole", "rolecreate"])
	@commands.bot_has_permissions(manage_roles=True)
	@commands.has_permissions(manage_roles=True)
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
		await ctx.message.delete()
	@commands.command()
	@commands.guild_only()
	async def mods(self, ctx):
		""" Check which mods are online on current guild """
		message = ""
		online, idle, dnd, offline = [], [], [], []

		for user in ctx.guild.members:
			if ctx.channel.permissions_for(user).kick_members or \
			   ctx.channel.permissions_for(user).ban_members:
				if not user.bot and user.status is discord.Status.online:
					online.append(f"**{user}**")
				if not user.bot and user.status is discord.Status.idle:
					idle.append(f"**{user}**")
				if not user.bot and user.status is discord.Status.dnd:
					dnd.append(f"**{user}**")
				if not user.bot and user.status is discord.Status.offline:
					offline.append(f"**{user}**")

		if online:
			message += f"Online {', '.join(online)}\n"
		if idle:
			message += f"idle {', '.join(idle)}\n"
		if dnd:
			message += f"DND {', '.join(dnd)}\n"
		if offline:
			message += f"Offline {', '.join(offline)}\n"

		await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")
	@commands.command()
	async def password(self, ctx, nbytes: int = 18):
		""" Generates a random password string for you
		This returns a random URL-safe text string, containing nbytes random bytes.
		The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
		"""
		if nbytes not in range(3, 1401):
			return await ctx.send("I only accept any numbers between 3-1400")
		if hasattr(ctx, 'guild') and ctx.guild is not None:
			await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
		await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")
	@commands.command()
	async def rate(self, ctx, *, thing: commands.clean_content):
		""" Rates what you desire """
		member = discord.Member
		rate_amount = random.uniform(0.0, 100.0)
		if thing == "Minecraft" or thing == "minecraft" or thing == "MC" or thing == "Mc" or thing == "mc":
			rate_amount = 98.88
		
		await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 4)} / 100**")
	@commands.command(name="botnick")
	@has_permissions(manage_nicknames=True)
	async def changebotnick(self, ctx, *, name : str):
		"""Change the bot nickname for the server"""
		# Let's get the bot's member in the current server
		botName = "{}#{}".format(self.bot.user.name, self.bot.user.discriminator)
		botMember = ctx.message.guild.get_member_named(botName)
		await botMember.edit(nick=str(name))
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
	@commands.command()
	@has_permissions(manage_roles=True)
	@bot_has_permissions(manage_roles=True)
	async def editrole(self, ctx, role:discord.Role, permissionvalue:int, pos:int, hoist:bool):
		"""Edit role. Args are role, permission value, role pos, and hoist."""
		value=permissionvalue
		try:
			perms = discord.Permissions(permissions=int(value))
		except:
			await ctx.send(Language.get("moderation.invalid_permission_number", ctx).format(value))
			return
		try:
			await role.edit(permissions=perms, position=pos, hoist=hoist)
			await ctx.send("Permissions Changed")
		except discord.errors.Forbidden:
			await ctx.send("Here")
			if role.position == ctx.me.top_role.position:
				await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
			elif role.position > ctx.me.top_role.position:
				await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
			else:
				await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
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
	@commands.command()
	@commands.guild_only()
	@has_permissions(manage_channels=True)
	async def createtc(self, ctx, name, slowmodetime : int):
		"""create a text channel. Args are name, and slowmodetime in seconds"""
		guild = ctx.guild
		await ctx.guild.create_text_channel(name=name, slowmode_delay=slowmodetime)
		embed=discord.Embed(title="Channel created", description="A Text Channel Named {} was made.".format(name), color=0xffc0cb)
		await ctx.send(embed=embed)
		for channel in guild.channels:
			if channel.name == "logs":
				await channel.send(embed=embed)
	@commands.command()
	@commands.guild_only()
	@has_permissions(manage_channels=True)
	async def createvc(self, ctx, name, bitrate:int, user_limit:int):
		"""Create a voice channel"""
		await ctx.guild.create_voice_channel(name=name, bitrate=bitrate, user_limit=user_limit)
		await ctx.send(f"A Voice Channel Named {name} was made")
	@commands.command()
	@has_permissions(manage_channels=True)
	async def edittc(self, ctx, newname):
		"""edit a text channel. Args are newname."""
		print("here")
		topic = "This is a channel created by Terrabot"
		await ctx.channel.edit(name=newname, topic=topic)
		embed=discord.Embed(title="Renamed Channel Successfully", description=f"The channel has been renamed to {newname}")
		await ctx.send(embed=embed)
	@commands.command()
	@has_permissions(manage_channels=True)
	async def mutechannelperms(self, ctx, role:discord.Role):
		"""Make users unable to send messages. Args are role."""
		await ctx.channel.set_permissions(role, attach_files=False, send_tts_messages=False, read_message_history=True, manage_messages=False, send_messages=False, read_messages=True, embed_links=False, manage_permissions=False)
		await ctx.send("Permissions updated for {}".format(role))
	# @commands.command()
	# async def integrate(self, ctx):
	# 	await ctx.guild.create_integration(type="YouTube", id=643)
	# 	await ctx.send("Successfully created an integration for YouTube.")

	@commands.command()
	@commands.is_owner()
	async def leaveguild(self, ctx, guild_id):
		guildtoleave = await self.bot.fetch_guild(guild_id)
		await guildtoleave.leave()
		await ctx.send(f"I have left the guild {guildtoleave}")
	@commands.command()
	@commands.has_permissions(manage_channels=True)
	async def deletetc(self, ctx, channelname:discord.TextChannel):
		await channelname.delete()
		await ctx.send(f"Channel {channelname} was deleted by {ctx.author}")
		for channel in ctx.guild.channels:
			if channel.name == "logs":
				await channel.send(f"Channel {channelname} was deleted by {ctx.author}")
def setup(bot):
	bot.add_cog(Admin(bot))