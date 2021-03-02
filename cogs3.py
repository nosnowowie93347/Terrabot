import discord, random
from discord import ext
from discord.ext import commands
from random import choice, randint
from discord.ext.commands import Bot
import platform, asyncio
class Cog3(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(description="Make fancy text!")
	async def fancify(self, ctx, *, text):
		def strip_non_ascii(string):
			"""Returns the string without non ASCII characters."""
			stripped = (c for c in string if 0 < ord(c) < 127)
			return ''.join(stripped)

		text = strip_non_ascii(text)
		if len(text.strip()) < 1:
			return await self.ctx.send(":x: ASCII characters only please!")
		output = ""
		for letter in text:
			if 65 <= ord(letter) <= 90:
				output += chr(ord(letter) + 119951)
			elif 97 <= ord(letter) <= 122:
				output += chr(ord(letter) + 119919)
			elif letter == " ":
				output += " "
		await ctx.send(output)
	@commands.command()
	@commands.guild_only()
	async def echotts(self, ctx, *, message):
		"""Makes the bot talk, with TTS."""
		say = message
		await ctx.message.delete()
		return await ctx.send(say, tts=True)
	@commands.command(
		name="echo",
		description="A simple command that repeats the users input back to them.",
	)
	@commands.guild_only()
	async def echo(self, ctx):
		await ctx.message.delete()
		embed = discord.Embed(
			title="Please tell me what you want me to repeat!",
			description="||This request will timeout after 1 minute.||",
		)
		sent = await ctx.send(embed=embed)

		try:
			msg = await self.bot.wait_for(
				"message",
				timeout=60,
				check=lambda message: message.author == ctx.author
				and message.channel == ctx.channel,
			)
			if msg:
				await sent.delete()
				await msg.delete()
				await ctx.send(msg.content)
		except asyncio.TimeoutError:
			await sent.delete()
			await ctx.send("Cancelling", delete_after=10)
	@commands.command()
	@commands.guild_only()
	async def roles(self, ctx):
		"""Lists the roles for the current guild"""
		roles = ctx.guild.roles
		embed = discord.Embed(title="**The roles on this server are: **")
		for role in roles:
			embed.add_field(name=role.name, value=role.name)
		await ctx.send(embed=embed)
	@commands.command(description="Really awful jokes. Courtesy of icanhazdadjoke.com")
	async def dadjoke(self, ctx):
		import requests
		channel = ctx.message.channel
		author  = ctx.message.author
		server  = ctx.message.guild
		joke = requests.get('https://icanhazdadjoke.com', headers={"Accept": "text/plain"}).text
		await ctx.send(joke)
	@commands.command(aliases=["diceroll", "rolladice"])
	async def roll(self, ctx):
		"""Roll a Frikin Die"""
		await ctx.send('You rolled a ' + str(randint(1,20)))
	@commands.command(aliases=["comic"])
	async def xkcd(self, ctx):
		"""Get ready to laugh... or somethin"""
		await ctx.send('get ready to laugh... or something')
		latest = requests.get('https://xkcd.com/info.0.json').json()
		num = random.randint(1, latest['num'])
		comic = requests.get('https://xkcd.com/' + str(num) + '/info.0.json').json()
		await ctx.send(comic['img'])
		await ctx.send('_' + comic['alt'] + '_')
	
def setup(bot):
	bot.add_cog(Cog3(bot))