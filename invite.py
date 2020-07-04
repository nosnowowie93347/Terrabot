# Make an invite link with 100 uses

import discord
from discord.ext import commands
import asyncio

class invite(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["invitelink", "serverlink", "link"])
	async def invite(self, ctx):
		"""Create invite to current server"""
		invitelinknew = await ctx.channel.create_invite(destination = ctx.message.channel, xkcd = True, max_uses = 100)
		print(invitelinknew)
		await ctx.send(invitelinknew)


def setup(bot):
	bot.add_cog(invite(bot))



