import discord, random, aiohttp, cat, hashlib, json, time, datetime, urllib, math, requests, asyncio, re, config, secrets, urllib, aiohttp, time, sys, importlib
from discord import ext
from random import choice
from Cogs import Settings
from io import BytesIO
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from PIL import Image
from utils.fun.fortunes import fortunes
from utils import imagetools
from utils.language import Language
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from utils2 import lists, permissions, http, default, argparser, dataIO
from utils.config import Config
from utils.tools import *
from utils import checks
config = Config()

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
	settings = bot.get_cog("Settings")
	bot.add_cog(Fun(bot, settings))


class Fun(commands.Cog):

	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

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
	async def insult(self, ctx):
		"""Says something mean about you."""
		await ctx.send(ctx.message.author.mention + " " + random.choice(config.insults))
	@commands.command()
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
				await ctx.message.delete()
				await author.send('`'+spoilified+'`')
	@commands.command()
	async def clone(self, ctx):
		'''
		Creates a webhook, that says what you say. Like echo.
		'''
		await ctx.message.delete()
		name="Terrabot updates all the time!"
		pfp = requests.get(ctx.author.avatar_url_as(format='png', size=256)).content
		hook = await ctx.channel.create_webhook(name=ctx.message.author,
												avatar=pfp)
		embed = discord.Embed(title="Message from Bot Owner", color=0x663399)
		embed.add_field(name="Terrabot updates all the time!", value=name)
		await hook.send(embed=embed)
		await hook.delete()
	@commands.command()
	async def updatenotice(self, ctx, role:discord.Role, *version:str):
		await ctx.message.delete()
		pfp = requests.get(ctx.author.avatar_url_as(format="png", size=256)).content
		hook = await ctx.channel.create_webhook(name="Terrabot Updater", avatar=pfp)
		embed = discord.Embed(title="Terrabot Updater", color=0x663399)
		embed.add_field(name="Terrabot has been updated to ", value=f"{version}")
		await hook.send(embed=embed)
		await hook.delete()
	@commands.command(aliases=["profile", "mcinfo"])
	async def minecraft(self, ctx, username):
		'''
		Shows MC account info, skin and username history
		'''
		import base64
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

	@commands.command()
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
	async def rolecall(self, ctx, role:discord.Role):
		role_embed = discord.Embed(color=role.color)
		role_embed.set_author(name='{}'.format(role.name))
		# We have a role
		members = [x for x in ctx.guild.members if role in x.roles]
		memberCount = len(members)
		memberOnline = len([x for x in members if x.status != discord.Status.offline])
		role_embed.add_field(name="Members", value='{:,} of {:,} online.'.format(memberOnline, memberCount), inline=True)
		await ctx.send(embed=role_embed)
	@commands.command(pass_context=True)
	@has_permissions(attach_files=True)
	async def log(self, ctx, messages : int = 25, *, chan : discord.TextChannel = None):
		
		logFile = 'discord.log'

		if not chan:
			chan = ctx

		# Remove original message
		await ctx.message.delete()

		mess = await ctx.send('Saving logs to *{}*...'.format(logFile))

		# Use logs_from instead of purge
		counter = 0
		msg = ''
		async for message in chan.history(limit=messages):
			counter += 1
			msg += message.content + "\n"
			msg += '----Sent-By: ' + message.author.name + '#' + message.author.discriminator + "\n"
			msg += '---------At: ' + message.created_at.strftime("%Y-%m-%d %H.%M") + "\n"
			if message.edited_at:
				msg += '--Edited-At: ' + message.edited_at.strftime("%Y-%m-%d %H.%M") + "\n"
			msg += '\n'

		msg = msg[:-2].encode("utf-8")

		with open(logFile, "wb") as myfile:
			myfile.write(msg)
		
		await mess.edit(content='Uploading *{}*...'.format(logFile))
		await ctx.author.send(file=discord.File(fp=logFile))
		await mess.edit(content='Uploaded *{}!*'.format(logFile))
		#os.remove(logFile)
	@commands.command()
	async def owo(self, ctx, *, text:str):
		"""OwO, owoify something >w<"""
		await ctx.send(owoify(text))
	@commands.command()
	async def spam3(self, ctx):
		"""SPAM SPAM SPAM"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/spam.png"))
	@commands.command()
	async def internetrules(self, ctx):
		"""The rules of the internet"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/InternetRules.txt"))
	
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
	@commands.command()
	async def cowsay(self, ctx, type:str, *, message:str):
		"""moo"""
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
	async def b1nzy(self, ctx):
		"""b1nzy pls no ;-;"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/b1nzy_with_banhammer.png"))
	@commands.command()
	async def honk(self, ctx):
		"""Honk honk mother fucka"""
		await ctx.send(random.choice(honkhonkfgt))
	@commands.command()
	async def headpat(self, ctx):
		"""Posts a random headpat from headp.at"""
		pats = requests.get("http://headp.at/js/pats.json").json()
		pat = random.choice(pats)
		file = url_to_bytes("http://headp.at/pats/{}".format(pat))
		await ctx.send(file=discord.File(file["content"], file["filename"]))
	@commands.command()
	async def twentyoneify(self, ctx, *, input:str):
		"""EVERYTHING NEEDS TWENTY ØNE PILØTS!"""
		await ctx.send(input.replace("O", "Ø").replace("o", "ø"))
	@commands.command()
	async def md5(self, ctx, *, msg:str):
		"""Convert something to MD5"""
		await ctx.send("`{}`".format(hashlib.md5(bytes(msg.encode("utf-8"))).hexdigest()))
	@commands.command()
	async def spotify(self, ctx, user:discord.Member=None):
		"""Get the current song that you or another user is playing"""
		if user is None:
			user = ctx.author
		activity = ctx.author.activity
		if activity is None:
			await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
			return
		if activity.type == discord.ActivityType.listening and activity.name == "Spotify":
			embed = discord.Embed(description="\u200b")
			embed.add_field(name="Artists", value=", ".join(activity.artists))
			embed.add_field(name="Album", value=activity.album)
			embed.add_field(name="Duration", value=str(activity.duration)[3:].split(".", 1)[0])
			embed.title = "**{}**".format(activity.title)
			embed.set_thumbnail(url=activity.album_cover_url)
			embed.url = "https://open.spotify.com/track/{}".format(activity.track_id)
			embed.color = activity.color
			embed.set_footer(text="{} - is currently playing this song".format(ctx.author.display_name), icon_url=get_avatar(ctx.author))
			await ctx.send(embed=embed)
		else:
			await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
			return
	@commands.command(hidden=True)
	async def infodebug(self, ctx, *, shit:str):
		"""This is the part where I make 20,000 typos before I get it right"""
		# "what the fuck is with your variable naming" - EJH2
		# seth seriously what the fuck - Robin
		import asyncio
		import os
		import random
		import re
		from datetime import datetime, timedelta
		try:
			rebug = eval(shit)
			if asyncio.iscoroutine(rebug):
				rebug = await rebug
			await ctx.send(py.format(rebug))
		except Exception as damnit:
			await ctx.send(py.format("{}: {}".format(type(damnit).__name__, damnit)))
	@commands.command()
	async def tableflip(self, ctx):
		# I hope this unicode doesn't break
		"""(╯°□°）╯︵ ┻━┻"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/tableflip.gif"))

	@commands.command()
	async def unflip(self, ctx):
		# I hope this unicode doesn't break
		"""┬─┬﻿ ノ( ゜-゜ノ)"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/unflip.gif"))
	@commands.command()
	async def actdrunk(self, ctx):
		"""I got drunk on halloween in 2016 it was great"""
		await ctx.send(random.choice(drunkaf))
	@commands.command()
	async def triggered(self, ctx):
		"""DID YOU JUST ASSUME MY GENDER? *TRIGGERED*"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/triggered.gif"))
	@commands.command()
	async def nolewding(self, ctx):
		"""No lewding!"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/nolewding.jpg"))
	@commands.command(hidden=True)
	async def what(self, ctx):
		"""what?"""
		await ctx.channel.trigger_typing()
		await ctx.send(file=discord.File("assets/imgs/reactions/what.gif"))
	@commands.command()
	@commands.is_nsfw()
	async def e621(self, ctx, *, tags:str):
		limit = config.max_nsfw_count

		"""Searches e621.net for the specified tagged images"""
		await ctx.channel.trigger_typing()
		try:
			data = requests.get("https://e621.net/post/index.json?limit={}&tags={}".format(limit, tags), headers=header).json()
		except json.JSONDecodeError:
			await ctx.send(Language.get("nsfw.no_results_found", ctx).format(tags))
			return
		count = len(data)
		if count == 0:
			await ctx.send(Language.get("nsfw.no_results_found", ctx).format(tags))
			return
		image_count = 4
		if count < 4:
			image_count = count
		images = []
		for i in range(image_count):
			images.append(data[random.randint(0, count)]["file_url"])
		await ctx.send(Language.get("nsfw.results", ctx).format(image_count, count, tags, "\n".join(images)))
	@commands.command()
	async def cat(self, ctx):
		cats = open("cats.py").read().splitlines()
		cat2 = random.choice(cats)
		
		await ctx.send(cat2)
	