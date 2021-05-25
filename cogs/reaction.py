import discord, asyncio, json, requests, typing
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot, bot_has_permissions, MissingPermissions, has_permissions
import emojis

class ReactionRolesNotSetup(commands.CommandError):
	"""reaction roles not setup for the current guild"""
	pass

def is_setup():
	async def wrap_func(ctx):
		data = await ctx.bot.config.find(ctx.guild.id)
		if data is None:
			raise ReactionRolesNotSetup

		if data.get("message_id") is None:
			raise ReactionRolesNotSetup

		return True

	return commands.check(wrap_func)


class Reactions(commands.Cog, name="ReactionRoles"):
	def __init__(self, bot):
		self.bot = bot
	
	async def rebuild_role_embed(self, guild_id):
		data = await self.bot.config.find(guild_id)
		channel_id = data["channel_id"]
		message_id = data["message_id"]

		guild = await self.bot.fetch_guild(guild_id)
		channel = await self.bot.fetch_channel(channel_id)
		message = await channel.fetch_message(message_id)

		embed = discord.Embed(title="Reaction Roles!")
		await message.clear_reactions()

		desc = ""
		reaction_roles = await self.bot.reaction_roles.get_all()
		reaction_roles = list(filter(lambda r: r["guild_id"] == guild_id, reaction_roles))

		for item in reaction_roles:
			role = guild.get_role(item["role"])
			desc += f"{item['_id']}: {role.mention}\n"
			await message.add_reaction(item["_id"])

		embed.description = desc
		await message.edit(embed=embed)


	async def get_current_reactions(self, guild_id):
		data = await self.bot.reaction_roles.get_all()
		data = filter(lambda r: r["guild_id"] == guild_id, data)
		data = map(lambda r: r["_id"], data)
		return list(data)

	@commands.group(
		aliases=['rr'], invoke_without_command=True
		)
	@commands.guild_only()
	async def reactionroles(self, ctx):
		await ctx.invoke(self.bot.get_command(name="help"), entity="reactionroles")

	@reactionroles.command(name="channel")
	@commands.guild_only()
	@commands.has_guild_permissions(manage_channels=True)
	async def rr_channel(self, ctx, channel: discord.TextChannel = None):
		if channel is None:
			await ctx.send("No channel given. Using current channel...")
		channel = channel or ctx.channel
		try:
			await channel.send("Testing if I can send messages here.", delete_after=0.05)
		except discord.HTTPException:
			await ctx.send("I cannot send messages to that channel! Try again after giving me permissions.")
			return

		embed = discord.Embed(title="Reaction Roles!")

		desc = ""
		reaction_roles = await self.bot.reaction_roles.get_all()
		reaction_roles = list(filter(lambda r: r['guild_id'] == ctx.guild.id, reaction_roles))
		for item in reaction_roles:
			role = ctx.guild.get_role(item["role"])
			desc += f"{item['_id']}: {role.mention}\n"
		embed.description = desc

		m = await ctx.send(embed=embed)
		for item in reaction_roles:
			await m.add_reaction(item["_id"])

		await self.bot.config.upsert(
			{
				"_id": ctx.guild.id,
				"message_id": m.id,
				"channel_id": m.channel.id,
				"is_enabled": True,
			}
		)
		await ctx.send("Should be all set up for you now!")
	@reactionroles.command(name="toggle")
	@commands.guild_only()
	@commands.has_guild_permissions(administrator=True)
	@is_setup()
	async def rr_toggle(self, ctx):
		data = await self.bot.config.find(ctx.guild.id)
		data["is_enabled"] = not data["is_enabled"]
		await self.bot.config.upsert(data)

		is_enabled = "enabled." if data["is_enabled"] else "disabled."
		await ctx.send(f"I've toggled that for you! It's currently {is_enabled}")
	@reactionroles.command(name="add")
	@commands.guild_only()
	@commands.has_guild_permissions(administrator=True)
	@is_setup()
	async def rr_add(self, ctx, emoji : typing.Union[discord.Emoji, str], *, role: discord.Role):
		reacts = await self.get_current_reactions(ctx.guild.id)
		if len(reacts) >= 20:
			await ctx.send("This does not support more than 20 Reaction roles per guild!")
		
		# if not isinstance(emoji, discord.Emoji):
		# 	emoji = emojis.get(emoji)
		# 	emoji = emoji.pop()

		if isinstance(emoji, discord.Emoji):
			if not emoji.is_usable():
				await ctx.send("I cannot use this emoji!")
				return

		emoji = str(emoji)
		await self.bot.reaction_roles.upsert({"_id": emoji, "role": role.id, "guild_id": ctx.guild.id})

		await self.rebuild_role_embed(ctx.guild.id)
		await ctx.send("This is added and good to go!")
	@reactionroles.command(name="remove")
	@commands.guild_only()
	@commands.has_guild_permissions(administrator=True)
	@is_setup()
	async def rr_remove(self, ctx, emoji : typing.Union[discord.Emoji, str]):
		if not isinstance(emoji, discord.Emoji):
			emoji = emojis.get(emoji)
			emoji = emoji.pop()

		emoji = str(emoji)
		await self.bot.reaction_roles.delete(emoji)
		await self.rebuild_role_embed(ctx.guild.id)
		await ctx.send("That should have been removed for you!")

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		data = await self.bot.config.find(payload.guild_id)

		if not payload.guild_id or not data or not data.get("is_enabled"):
			return

		guild_reaction_roles = await self.get_current_reactions(payload.guild_id)
		if str(payload.emoji) not in guild_reaction_roles:
			return

		guild = await self.bot.fetch_guild(payload.guild_id)

		emoji_data = await self.bot.reaction_roles.find(str(payload.emoji))
		role = guild.get_role(emoji_data["role"])

		member = await guild.fetch_member(payload.user_id)

		if role not in member.roles:
			await member.add_roles(role, reason="Reaction role.")

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		data = await self.bot.config.find(payload.guild_id)

		if not payload.guild_id or not data or not data.get("is_enabled"):
			return

		guild_reaction_roles = await self.get_current_reactions(payload.guild_id)
		if str(payload.emoji) not in guild_reaction_roles:
			return

		guild = await self.bot.fetch_guild(payload.guild_id)

		emoji_data = await self.bot.reaction_roles.find(str(payload.emoji))
		role = guild.get_role(emoji_data["role"])

		member = await guild.fetch_member(payload.user_id)

		if role in member.roles:
			await member.remove_roles(role, reason="Reaction role.")
def setup(bot):
	bot.add_cog(Reactions(bot))
