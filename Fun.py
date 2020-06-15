import discord, random, aiohttp, json, time, datetime, urllib, math, requests, asyncio, re, config, secrets, urllib, aiohttp, time, sys, importlib
from discord import ext
from random import choice
from Cogs import Settings
from io import BytesIO
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
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
	@commands.command(pass_context=True)
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

