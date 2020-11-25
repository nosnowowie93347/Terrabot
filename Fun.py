import discord, random, speedtest, base64, aiohttp, cat, hashlib, json, time, datetime, urllib, math, requests, asyncio, re, secrets, urllib, aiohttp, time, sys, importlib, os
from discord import ext
import humanize as h
from random import choice
from io import BytesIO
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from PIL import Image
from utils.fun.fortunes import fortunes
from utils import imagetools, checks, config
from utils.language import Language
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from utils2 import lists, permissions, http, default, argparser, dataIO
coinsides = ['Heads', 'Tails']
random_word = random.choice("words.txt")
lines = open('words.txt').read().splitlines()
dabs = [
  "https://cdn.discordapp.com/attachments/554560461933248514/632891549578952714/2Q.png",
  "https://cdn.discordapp.com/attachments/554560461933248514/632891753690562562/2Q.png"
]
punlist = open("Punlist.txt", encoding='utf8').read().splitlines()
compliments = open("Compliments.txt", encoding='utf8').read().splitlines()

def setup(bot):
	bot.add_cog(Fun(bot))


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
	@commands.command()
	async def greeting(self, ctx):
		greeting = ["Hello! Today is a good day", "Hello! Today is a bad day"]
		await ctx.send(random.choice(greeting))
	@commands.command(hidden=True)
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
	@commands.command()
	async def rps(self, ctx, choice: str):
		"""Play rock-paper-scissors"""
		try:
			userChoice = choice.lower()

			if userChoice != "rock" and userChoice != "paper" and userChoice != "scissors":
				await ctx.send("You can only choose from rock, paper or scissors")
			else:
				temp = random.randint(1, 3)
				if temp == 1:
					botChoice = "rock"
				elif temp == 2:
					botChoice = "paper"
				elif temp == 3:
					botChoice = "scissors"

				# This is kind of ugly but it works
				if userChoice == botChoice:
					await ctx.send("I choose **{}**. The game was a tie!".format(botChoice))
				elif userChoice == "rock":
					if botChoice == "paper":
						await ctx.send("I choose **{}**. I win!".format(botChoice))
					elif botChoice == "scissors":
						await ctx.send("I choose **{}**. You win!".format(botChoice))
				elif userChoice == "paper":
					if botChoice == "scissors":
						await ctx.send("I choose **{}**. I win!".format(botChoice))
					elif botChoice == "rock":
						await ctx.send("I choose **{}**. You win!".format(botChoice))
				elif userChoice == "scissors":
					if botChoice == "rock":
						await ctx.send("I choose **{}**. I win!".format(botChoice))
					elif botChoice == "paper":
						await ctx.send("I choose **{}**. You win!".format(botChoice))
		except Exception as e:
			await ctx.send(e)
	@commands.command()
	async def Creeper(self, ctx):
		"""So we back in the mine..."""
		await ctx.send("Aww man")
	@commands.command()
	async def insult(self, ctx, member:discord.Member):
		"""Says something mean about you."""
		await ctx.send(member.mention + " " + random.choice(config.insults))
	@commands.command()
	async def roast(self, ctx, member : discord.Member):
		"""Less awful version of the insult command"""
		await ctx.send(random.choice(lines))
	@commands.command()
	async def coinflip(self, ctx):
		"""Flip a Frikin Coin"""
		await ctx.send(random.choice(coinsides))

	@commands.command()
	async def dab(self, ctx):
		"""Dab on them haters!"""
		response = random.choice(dabs)
		await ctx.send(random.choice(dabs))
		print(f"Dabbed on behalf of {ctx.author}.")
		await ctx.send(f"Dabbed on behalf of {ctx.author}.")
	@commands.command(hidden=True)
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
	@commands.command(hidden=True)
	async def getbotprefix(self, ctx):
		"""Gets the prefixes of the bot"""
		message = discord.Message
		prefix = await self.bot.get_prefix(message)
		await ctx.send(f"My prefix is {prefix}")
	@commands.command(hidden=True, aliases=["changeavatar", "newavatar"])
	@commands.cooldown(1, 654, commands.BucketType.guild)
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
	
	@commands.command(aliases=["directmessage", "pm"])
	@commands.cooldown(1, 35, commands.BucketType.user)
	async def dm(self, ctx, member:discord.User, *, message: str):
		""" DM the user of your choice """
		user = member
		if not user:
			return await ctx.send(f"Could not find any UserID matching **{user_id}**")

		try:
			# if not role in user.roles:
			await user.send(message)
			# if role in user.roles:
			# 	return await ctx.send("This user has the no dm role. This means they probably don't want DMs.")
			await ctx.send(f"✉️ Sent a DM to **{member.name}**")
			await user.send(f"Message sent by: {ctx.author}")
			await user.send(f"Sent from {ctx.guild.name}")
		except discord.Forbidden:
			await ctx.send("This user might be having DMs blocked or it's a bot account...")
	@commands.command()
	async def emojify(self, ctx, *, text: str):
		'''
		Converts the alphabet and spaces into emoji
		'''
		author = ctx.message.author
		emojified = '⬇ Copy and paste this: ⬇\n'
		formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
		if text == '':
			await ctx.send('Remember to say what you want to convert!')
		else:
			for i in formatted:
				if i == ' ':
					emojified += '     '
				else:
					emojified += ':regional_indicator_{}: '.format(i)
			if len(emojified) + 2 >= 2000:
				await ctx.send('Your message in emojis exceeds 2000 characters!')
			if len(emojified) <= 25:
				await ctx.send('Your message could not be converted!')
			else:
				await ctx.send('`'+emojified+'`')
	@commands.command()
	async def spoilify(self, ctx, *, text: str):
		'''
		Converts the alphabet and spaces into hidden secrets
		'''
		author = ctx.message.author
		spoilified = '⬇ Copy and paste this: ⬇\n'
		if text == '':
			await ctx.send('Remember to say what you want to convert!')
		else:
			for i in text:
				spoilified += '||{}||'.format(i)
			if len(spoilified) + 2 >= 2000:
				await ctx.send('Your message in spoilers exceeds 2000 characters!')
			if len(spoilified) <= 4:
				await ctx.send('Your message could not be converted!')
			else:
				await author.send('`'+spoilified+'`')
	@commands.command(aliases=["mcprofile", "mcinfo"])
	async def minecraft(self, ctx, username):
		'''
		Shows MC account info, skin and username history
		'''
		try:
			uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
								.format(username)).json()['id']

			url = json.loads(base64.b64decode(requests.get(
				'https://sessionserver.mojang.com/session/minecraft/profile/{}'
				.format(uuid)).json()['properties'][0]['value'])
							 .decode('utf-8'))['textures']['SKIN']['url']
			
			names = requests.get('https://api.mojang.com/user/profiles/{}/names'
								.format(uuid)).json()
			history = "**Name History:**\n"
			for name in reversed(names):
				history += name['name']+"\n"

			await ctx.send('**Username: `{}`**\n**Skin: {}**\n**UUID: {}**'.format(username, url, uuid))
			await ctx.send(history)
		except ValueError as e:
			await ctx.send(e)
			await asyncio.sleep(2)
			await ctx.send("This means the profile wasn't found...")

	@commands.command(aliases=["wiki"])
	async def wikipedia(self, ctx, *, query: str):
		'''
		Uses Wikipedia APIs to summarise search
		'''
		sea = requests.get(
			('https://en.wikipedia.org//w/api.php?action=query'
			 '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
			).format(query)).json()['query']

		if sea['searchinfo']['totalhits'] == 0:
			await ctx.send('Sorry, your search could not be found.')
		else:
			for x in range(len(sea['search'])):
				article = sea['search'][x]['title']
				req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
								   '&utf8=1&redirects&format=json&prop=info|images'
								   '&inprop=url&titles={}'.format(article)).json()['query']['pages']
				if str(list(req)[0]) != "-1":
					break
			else:
				await ctx.send('Sorry, your search could not be found.')
				return
			article = req[list(req)[0]]['title']
			arturl = req[list(req)[0]]['fullurl']
			artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
			lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
			embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0x3FCAFF)
			embed.set_footer(text='Wiki entry last modified',
							 icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
			embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
							 icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
			embed.timestamp = lastedited
			await ctx.send('**Search result for:** ***"{}"***:'.format(query), embed=embed)
	@commands.command(pass_context=True, hidden=True)
	async def listmuted(self, ctx):
		"""Lists the names of those that are muted."""
		role = discord.utils.get(ctx.guild.roles, name='Muted')
		muteList = role.members

		if not len(muteList):
			await ctx.send("No one is currently muted.")
			return

		# We have at least one member muted
		msg = 'Currently muted:\n\n'
		msg += ', '.join([member.name for member in muteList])

		await ctx.send(msg)
	@commands.command()
	async def rolecall(self, ctx, *, role:discord.Role):
		"""Number of online members in a role"""
		role_embed = discord.Embed(color=role.color)
		role_embed.set_author(name='{}'.format(role.name))
		# We have a role
		members = [x for x in ctx.guild.members if role in x.roles]
		memberCount = len(members)
		memberOnline = len([x for x in members if x.status != discord.Status.offline])
		role_embed.add_field(name="Members", value='{:,} of {:,} online.'.format(memberOnline, memberCount), inline=True)
		await ctx.send(embed=role_embed)
	@commands.command()
	async def owo(self, ctx, *, text:str):
		"""OwO, owoify something >w<"""
		await ctx.send(owoify(text))
	@commands.command()
	async def fight(self, ctx, user:str=None, *, weapon:str=None):
		"""Fight someone with something"""
		if user is None or user.lower() == ctx.author.mention or user == ctx.author.name.lower() or ctx.guild is not None and ctx.author.nick is not None and user == ctx.author.nick.lower():
			await ctx.send("{} fought themself but only ended up in a mental hospital!".format(ctx.author.mention))
			return
		if weapon is None:
			await ctx.send("{0} tried to fight {1} with nothing so {1} beat the breaks off of them!".format(ctx.author.mention, user))
			return
		await ctx.send("{} used **{}** on **{}** {}".format(ctx.author.mention, weapon, user, random.choice(fight_results).replace("%user%", user).replace("%attacker%", ctx.author.mention)))
	@commands.command(description="moo", help="use the cows command to list the different types", usage="[type] [message]")
	async def cowsay(self, ctx, type:str, *, message:str):
		try:
			cow = cowList[type.lower()]
		except KeyError:
			await ctx.send("`{}` is not a usable character type. Run **{}cows** for a list of cows.".format(type, ctx.prefix))
			return
		msg = "```{}```".format(cow.milk(message))
		if len(msg) > 2000:
			await ctx.send("Sorry, the message length with the cow in it has a total character length of {}. Discord only allows 2000 characters per message.".format(len(msg)))
			return
		await ctx.send(msg)
	@commands.command()
	async def cows(self, ctx):
		"""Cow list for the cowsay command"""
		await ctx.send("Current list of cows:```{}```".format(", ".join(cowList.keys())))
	@commands.command()
	async def trigger(self, ctx, *, member:discord.Member=None):
		"""Triggers a user"""
		await ctx.channel.trigger_typing()
		if member is None:
			member = ctx.author
		download_file(get_avatar(member, animate=False), "data/trigger.png")
		avatar = Image.open("data/trigger.png")
		triggered = imagetools.rescale(Image.open("assets/imgs/pillow/triggered.jpg"), avatar.size)
		position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
		avatar.paste(triggered, position)
		avatar.save("data/trigger.png")
		await ctx.send(file=discord.File("data/trigger.png"))
	@commands.command()
	async def tableflip(self, ctx):
		# I hope this unicode doesn't break
		"""(╯°□°）╯︵ ┻━┻"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/tableflip.gif"))
	
	@commands.command(aliases=['speedtest', 'speed'],help='Shows Information about the system that the bot is running on')
	@commands.cooldown(1, 10, commands.BucketType.guild)
	async def system(self,msg):
		Speed = speedtest.Speedtest()
		Speed.get_best_server()

		upload = Speed.upload(threads=None)
		download = Speed.download(threads=None)

		try:

			em = discord.Embed(color=discord.Color.red(), title="System Connection Speed",)

			em.add_field(name="System Connection info",value=f"{h.naturalsize(download)}/s Down {h.naturalsize(upload)}/s Up",inline=True)


			await msg.send(embed=em)
		except Exception as e:
			await msg.send(f"Failed to get system info: {e} ")
	@commands.command()
	async def unflip(self, ctx):
		# I hope this unicode doesn't break
		"""┬─┬﻿ ノ( ゜-゜ノ)"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/unflip.gif"))
	@commands.command(enabled=False)
	async def actdrunk(self, ctx):
		"""I got drunk on halloween in 2016 it was great"""
		await ctx.send(random.choice(drunkaf))
	@commands.command()
	async def triggered(self, ctx):
		"""DID YOU JUST ASSUME MY GENDER? *TRIGGERED*"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/triggered.gif"))
	@commands.command()
	async def cat(self, ctx):
		"""Like the shibe command, but with cats."""
		cats = open("cats.py").read().splitlines()
		cat2 = random.choice(cats)
		
		await ctx.send(cat2)
	@commands.command(enabled=False)
	async def heal(self, ctx, member:discord.Member):
		"""Heals a person. NOTE: Just for fun."""
		await ctx.send(f"Attempting to heal {member.mention}")
		await asyncio.sleep(3)
		options = ["Healing Failed", "Yay! It worked!"]
		await ctx.send(random.choice(options))
	@commands.command()
	async def feed(self, ctx, member:discord.Member, *, food):
		"""Feed someone. NOTE: Just for fun"""
		await ctx.send("Fed {} {}".format(member, food))
	@commands.command()
	async def areyoutired(self, ctx):
		"""Is the bot tired?"""
		yes = "yes"
		no = "no"
		await ctx.send(random.choice([yes, no]))
	@commands.command()
	async def timetravel(self, ctx, numofminutes:int):
		"""Just don't mess up the timeline..."""
		await ctx.send(f"skipping forward {numofminutes} minutes", delete_after=35)
	@commands.command(description="What time is it?")
	async def clock(self, ctx):
		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		await ctx.send(f"now = {current_time}")