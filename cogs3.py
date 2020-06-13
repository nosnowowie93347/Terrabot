import discord, random
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot
import platform, asyncio
class Cog3(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def fancify(self, ctx, *, text):
		"""Makes text fancy!"""
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
	@commands.command(aliases=['saytts'])
	async def echotts(self, ctx, *, message):
		"""Makes the bot talk, with TTS."""
		say = message
		await ctx.message.delete()
		return await ctx.send(say, tts=True)
	@commands.command(aliases=['say'])
	async def echo(self, ctx, *, message):
		"""Makes the bot talk."""
		say = message
		await ctx.message.delete()
		return await ctx.send(say)
	@commands.command()
	async def roles(self, ctx):
		roles = ctx.guild.roles
		result = "**The roles on this server are: **"
		for role in roles:
			result += role.name + ", "
		await ctx.send(result)
	@commands.command()
	async def dadjoke(self, ctx):
		"""Really awful jokes. Courtesy of icanhazdadjoke.com"""
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
		await ctx.send('get ready to laugh... or something')
		latest = requests.get('https://xkcd.com/info.0.json').json()
		num = random.randint(1, latest['num'])
		comic = requests.get('https://xkcd.com/' + str(num) + '/info.0.json').json()
		await ctx.send(comic['img'])
		await ctx.send('_' + comic['alt'] + '_')
	@commands.command(aliases=["areyouworking"])
	async def test(self, ctx):
		await ctx.send('This Bot is Working (Dispite what Ruby might tell you)')
	@commands.command(aliases=["naptime", "sleepytime"])
	async def sleep(self, ctx):
		await ctx.send(":sleeping:")
		await asyncio.sleep(5)
		await ctx.send('Done sleeping')
		await ctx.send("Wow! That was quite the nap.")
		
def setup(bot):
	bot.add_cog(Cog3(bot))