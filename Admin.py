import logging, random, logging, discord, asyncio, secrets
from io import BytesIO
from discord import ext
from random import randint, choice
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["bannedusers"])
	async def getbans(self, ctx):
		import config
		"""Lists banned members"""
		if ctx.message.author.guild_permissions.ban_members:
			x = await ctx.guild.bans()
			x = '\n'.join([str(y.user) for y in x])
			thing3 = "List of Banned Members\n" + x
			await ctx.send(thing3)
		else:
			await ctx.send(config.errormessage)
	@commands.command(aliases=["permkick", "permaban"])
	async def ban(self, ctx, member : discord.Member, *,  reason : str):
		"""When you're just not having it"""
		await member.ban(reason = reason)
		banembed=discord.Embed(title=f"{member} banned successfully", description=f"{member} banned for {reason}")
		await ctx.send(embed=banembed)
	@commands.command()
	@has_permissions(ban_members=True)
	async def hackban(self, ctx, member : discord.Object, *, reason : str):
		"""Ban ppl by id"""
		await ctx.guild.ban(member, reason=reason)
		embed = discord.Embed(title=f"Successfully banned {member}", description=f"{member} banned for {reason}", color=0xff00f6)
		await ctx.send(embed=embed)
		await ctx.message.delete()
	@commands.command(name="kick")
	async def kick(self, ctx, member : discord.Member, *, reason : str):
		"""Kicks a user"""
		await member.kick(reason=reason)
		description = f"You've been bad, {member.mention}. You've been kicked."
		kickembed = discord.Embed(title="User kicked", description=description, color=0xf6d025, footer="Powered by: Terrabot")
		await ctx.send(embed=kickembed)
		logger.info(f"You've been bad, {member.mention}. You've been kicked.")
	@commands.command()
	@has_permissions(manage_roles=True)
	async def addrole(self, ctx, member: discord.Member, *, role:discord.Role):
		"""Adds a role to a user"""
		await member.add_roles(role)
		await ctx.send(f"Added {role} to {member}")
	@commands.command()
	async def unban(self, ctx, member : discord.Object, *, reason : str):
		"""Unbans a user"""
		await ctx.guild.unban(member, reason=reason)
		description = f"Yay! {member} was unbanned"
		embed = discord.Embed(title="Member Unbanned", description=description)
	@commands.command(name='mute')
	@has_permissions(manage_nicknames=True)
	async def mute_cmd(self, ctx, member: discord.Member):
		"""Mute ppl who break the rules"""
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
		await member.add_roles(role)
		embed = discord.Embed(title = 'User Muted',color = 0xff00f6,description = f'{member.mention} was muted by {ctx.author.mention}')
		return await ctx.send(embed=embed)
		logger.info("Muted {} for {}".format(member, reason))
	@commands.command(name="unmute")
	@has_permissions(manage_roles=True)
	async def unmute_command(self, ctx, member : discord.Member):
		"""Unmute. Just in case."""
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		if not role:
			await ctx.send("User not muted")
			return await ctx.send(f"Unable to mute {ctx.author} - No role found")
		if role in member.roles:
			await member.remove_roles(role)
			embed = discord.Embed(title= "User Unmuted", color=0xff00f6,description= f'{member.mention} was unmuted by {ctx.author.mention}')
			await ctx.send(embed=embed)
	@commands.command()
	@has_permissions(manage_roles=True)
	async def unwarn(self, ctx, member:discord.Member, *, reason:str):
		embed=discord.Embed(title="Unwarned User", description="Unwarned {} for {}".format(member.mention, reason))
		role = discord.utils.get(ctx.guild.roles, name="Warned")
		await member.remove_roles(role)
		await ctx.send(embed=embed)
		logger.info("Warned {} for {}".format(member, reason))
	@commands.command()
	async def warn(self, ctx, member:discord.Member, *, reason:str):
		"""Step before mute"""
		embed = discord.Embed(title="Warned User", color=0xff00f6,description=f'{member.mention} was warned by {ctx.author.mention}')
		role = discord.utils.get(ctx.guild.roles, name='Warned')
		await member.add_roles(role)
		await ctx.send(embed=embed)
		logger.info("Warned {} for {}".format(member, reason))
	@commands.command()
	@commands.bot_has_permissions(manage_roles=True)
	@commands.has_permissions(manage_guild=True)
	async def removerole(self, ctx, member:discord.Member, *, rolename:discord.Role):
		guild = ctx.guild
		author = ctx.message.author
		await member.remove_roles(rolename, reason=None)
		embed=discord.Embed(title="Role removed", description="Role {} removed from {}".format(rolename, member), color=0xf6d025, footer="Powered by Terrabot")
		await ctx.send(embed=embed)
	@commands.command(aliases=["createrole", "rolecreate"])
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
	async def changebotnick(self, ctx, *, name : str):
		# Let's get the bot's member in the current server
		botName = "{}#{}".format(self.bot.user.name, self.bot.user.discriminator)
		botMember = ctx.message.guild.get_member_named(botName)
		await botMember.edit(nick=str(name))
def setup(bot):
	bot.add_cog(Admin(bot))