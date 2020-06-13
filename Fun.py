import discord, random, asyncio, config, secrets, urllib, aiohttp, time, sys, importlib
from discord import ext
from random import choice
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import Bot
from utils import lists, permissions, http, default, argparser, dataIO
coinsides = ['Heads', 'Tails']
random_word = random.choice("words.txt")
lines = open('words.txt').read().splitlines()
dabs = [
  "https://cdn.discordapp.com/attachments/554560461933248514/632891549578952714/2Q.png",
  "https://cdn.discordapp.com/attachments/554560461933248514/632891753690562562/2Q.png"
]
punlist = open("Punlist.txt", encoding='utf8').read().splitlines()
compliments = open("Compliments.txt", encoding='utf8').read().splitlines()
class Fun(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def groot(self, ctx):
		"""Who... who are you?"""
		groots = [
			"I am Groot",
			"**I AM GROOT**",
			"I... am... *Groot*",
			"I am Grooooot",
		]
		punct = [
			"!",
			".",
			"?"
		]
		# Build our groots
		groot_max = 5
		groot = " ".join([random.choice(groots) + (random.choice(punct)*random.randint(0, 5)) for x in range(random.randint(1, groot_max))])
		await ctx.send(groot)
	@commands.command(aliases=["greet"])
	async def greeting(self, ctx):
		greeting = ["Hello! Today is a good day", "Hello! Today is a bad day"]
		await ctx.send(random.choice(greeting))
	@commands.command()
	async def compliment(self, ctx, member : discord.Member):
		"""Says something nice"""
		await ctx.send(random.choice(compliments))
	@commands.command()
	async def pun(self, ctx):
		"""Grab a EGG-celent pun..."""
		await ctx.send(random.choice(punlist))
	@commands.command(aliases=["quoteoftheday", "inspireme"])
	async def qotd(self, ctx):
		"""Quotes to get you through the day"""
		Quotes = open("Quotes.txt", encoding='utf8').read().splitlines()
		await ctx.send(random.choice(Quotes))
	@commands.command(aliases=["roshambo", "rockpaperscissors"])
	async def rps(self, ctx, message):
		"""Rock paper scissors with the bot."""
		choices = ["rock", "paper", "scissors"]
		await ctx.send(random.choice(choices))
	@commands.command(aliases=["revenge", "creeper"])
	async def Creeper(self, ctx):
		"""So we back in the mine..."""
		await ctx.send("Aww man")
	@commands.command(aliases=["biggerroast"])
	async def insult(self, ctx):
		"""Says something mean about you."""
		await ctx.send(ctx.message.author.mention + " " + random.choice(config.insults))
	@commands.command(aliases=["roastme", "ineedaroast", "bully"])
	async def roast(self, ctx, member : discord.Member):
		"""Less awful version of the insult command"""
		await ctx.send(random.choice(lines))
	@commands.command(aliases=["flipacoin", "headsortails", "flippadacoin"])
	async def coinflip(self, ctx):
		"""Flip a Frikin Coin"""
		await ctx.send(random.choice(coinsides))

	@commands.command()
	async def dab(self, ctx):
		"""Dab on them haters!"""
		response = random.choice(dabs)
		await ctx.send(random.choice(dabs))
		print(f"Dabbed on behalf of {ctx.author}.")
	@commands.command()
	async def minecraftquotes(self, ctx):
		"""Amazing quotes from 50 Ways to Die in Minecraft"""
		waystodie = open("waystodie.txt").read().splitlines()
		await ctx.send(random.choice(waystodie))
	@commands.command(aliases=['howhot', 'hot'])
	async def hotcalc(self, ctx, *, user: discord.Member = None):
		""" Returns a random percent for how hot is a discord user """
		user = user or ctx.author

		random.seed(user.id)
		r = random.randint(1, 100)
		hot = r / 1.17

		emoji = "💔"
		if hot > 25:
			emoji = "❤"
		if hot > 50:
			emoji = "💖"
		if hot > 75:
			emoji = "💞"

		await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
	@commands.command()
	async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
		""" Make a fake Supreme logo
		Arguments:
			--dark | Make the background to dark colour
			--light | Make background to light and text to dark colour
		"""
		parser = argparser.Arguments()
		parser.add_argument('input', nargs="+", default=None)
		parser.add_argument('-d', '--dark', action='store_true')
		parser.add_argument('-l', '--light', action='store_true')

		args, valid_check = parser.parse_args(text)
		if not valid_check:
			return await ctx.send(args)

		inputText = urllib.parse.quote(' '.join(args.input))
		if len(inputText) > 500:
			return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

		darkorlight = ""
		if args.dark:
			darkorlight = "dark=true"
		if args.light:
			darkorlight = "light=true"
		if args.dark and args.light:
			return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

		await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png")
	async def randomimageapi(self, ctx, url, endpoint):
		try:
			r = await http.get(url, res_method="json", no_cache=True)
		except aiohttp.ClientConnectorError:
			return await ctx.send("The API seems to be down...")
		except aiohttp.ContentTypeError:
			return await ctx.send("The API returned an error or didn't return JSON...")

		await ctx.send(r[endpoint])

	async def api_img_creator(self, ctx, url, filename, content=None):
		async with ctx.channel.typing():
			req = await http.get(url, res_method="read")

			if req is None:
				return await ctx.send("I couldn't create the image ;-;")

			bio = BytesIO(req)
			bio.seek(0)
			await ctx.send(content=content, file=discord.File(bio, filename=filename))
	@commands.command()
	async def change_avatar(self, ctx, url: str = None):
		""" Change avatar. """
		if url is None and len(ctx.message.attachments) == 1:
			url = ctx.message.attachments[0].url
		else:
			url = url.strip('<>') if url else None

		try:
			bio = await http.get(url, res_method="read")
			await self.bot.user.edit(avatar=bio)
			await ctx.send(f"Successfully changed the avatar. Currently using:\n{url}")
		except aiohttp.InvalidURL:
			await ctx.send("The URL is invalid...")
		except discord.InvalidArgument:
			await ctx.send("This URL does not contain a useable image")
		except discord.HTTPException as err:
			await ctx.send(err)
		except TypeError:
			await ctx.send("You need to either provide an image URL or upload one with the command")
	@commands.command()
	async def dm(self, ctx, user_id: int, *, message: str):
		""" DM the user of your choice """
		user = self.bot.get_user(user_id)
		if not user:
			return await ctx.send(f"Could not find any UserID matching **{user_id}**")

		try:
			await user.send(message)
			await ctx.send(f"✉️ Sent a DM to **{user_id}**")
		except discord.Forbidden:
			await ctx.send("This user might be having DMs blocked or it's a bot account...")
def setup(bot):
	bot.add_cog(Fun(bot))