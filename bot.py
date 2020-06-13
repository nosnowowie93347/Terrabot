import discord, platform, asyncio, psutil, time, requests, urllib.request, logging, json, typing, random, os, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct
from discord import *
import config
from   PIL         import Image
from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
					ZeroOrMore,Forward,nums,alphas,oneOf)
import math
import operator
from Cogs import TinyURL, Settings, Message, DL, ReadableTime, ProgressBar, GetImage, ComicHelper, Utils, Nullify, DisplayName, UserTime, PickList
from random import choice, randint, randrange
from discord.ext import commands
from discord.ext.commands import Bot
import discord.utils
from discord.utils import get
from   discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
import datetime


import pyfiglet, time
from pyfiglet import figlet_format, FontNotFound
import datetime as dt

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()
today = datetime.date.today()
bot = discord.ext.commands.Bot(command_prefix='^', description="Hello my name is Terrabot")
now = datetime.datetime.now()

moveoutday = datetime.datetime(now.year, 8, 10) - \
	datetime.datetime.today()#days till i move out
diff = datetime.datetime(now.year, 12, 25) - \
	datetime.datetime.today() #days till christmas
diff2 = datetime.datetime(now.year, 4, 12) - \
	datetime.datetime.today() #days till easter
journeysend = datetime.datetime(now.year, 5, 16) - \
	datetime.datetime.today() #days till journey's end
optionsforchristmascountdown = ['%xmas', "%xmascd", '%christmas']
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
cmds = open('commands.py', encoding= 'utf8').read().splitlines()
choices = ['rock', 'paper', 'scissors']

now_playing = "Playing Convincing Everyone I'm Better than Risabot."
rockpaperscissors = random.choice(choices)
random_word = random.choice("words.txt")
lines = open('words.txt').read().splitlines()
startTime = int(time.time())
compliments = open("Compliments.txt", encoding='utf8').read().splitlines()
myline = random.choice(lines)
memes = open("memes2.py", encoding='utf8').read().splitlines()
meme = random.choice(memes)
@bot.event
async def on_ready():
	print("Hey! I'm Terrabot!")
	print("I'm made by Pinkalicious21902")
	print("Who's ready to have a good time?")
	bot.load_extension("EightBall")
	bot.load_extension("Comics")
	bot.load_extension("cog2")
	bot.load_extension("cogs3")
	bot.load_extension("Fun")
	bot.load_extension("Encode")
	bot.load_extension("invite")
	bot.load_extension("emojis")
	bot.load_extension("Morecogs")
	bot.load_extension("Morse")
	bot.load_extension("Botstuff")
	bot.load_extension("Admin")
	bot.load_extension("Translate")
	bot.load_extension("cogs4")
	await bot.change_presence(activity=discord.Game(name="Serving Pinkalicious21902 Forever and Always"), status=discord.Status.online)
	print(time.time())
@bot.event
async def on_message(message):
	swearwords = ["shit", "cock", "porn", "dick", "ass", "slut", "pussy", "bitch", "cunt", "fuck", "fag", "bastard", "sex", "retard", "vagina"]
	for word in swearwords:
		if word in message.content:
			await message.delete()
			await message.channel.send("Hey! watch the language")
			

	# if message.content.startswith("how dare u disrespect your master"):
	# 	await message.channel.send("I'm NOT sorry")
	# if message.content.startswith("x&"):
	# 	await message.delete(delay=None)
	# 	embed=discord.Embed(title="Nice try. Ruby's been blocked")
	# 	await message.channel.send(embed=embed)
	# 	await message.channel.send("You block mine, I block urs. From Pink.")
	if bot.user.mentioned_in(message):
		await message.channel.send("REEEEEE! I don't like being pinged. \npls use prefix instead.")
	await bot.process_commands(message)
@bot.event
async def on_reaction_add(reaction, user):
		bot.dispatch("picklist_reaction", reaction, user)
def eval(num_string,parseAll=True):
		exprStack=[]
		results=bnf.parseString(num_string,parseAll)
		val=evaluateStack(exprStack[:] )
		return val

def buildDilbertURL(date):
	return "http://dilbert.com/strip/" + str(date['Year']) + "-" + str(date['Month']) + "-" + str(date['Day'])
	
  # ####### #
 # Dilbert #
# ####### #
def quote(query):
		# Strips all spaces, tabs, returns and replaces with + signs, then urllib quotes
		return query.replace("+","%2B").replace("\t","+").replace("\r","+").replace("\n","+").replace(" ","+")

	
async def get_search(ctx, query, service=""):
		# Searches in the passed service
		service = "s={}&".format(service) if service else ""
		lmgtfy = "http://lmgtfy.com/?{}q={}".format(service, quote(query))
		try:
			lmgtfyT = await TinyURL.tiny_url(lmgtfy, bot)
		except Exception as e:
			print(e)
			msg = "It looks like I couldn't search for that... :("
		else:
			msg = '*{}*, you can find your answers here:\n\n<{}>'.format((ctx.message.author), lmgtfyT)
		return msg
@bot.command(aliases=["wipe", "delete", "clean", "removespam", "deletemsgs"])
@commands.has_permissions(manage_messages=True)
@commands.is_owner()
async def purge(ctx, number: int):
	"""Deletes a certain number of messages"""
	await ctx.trigger_typing()
	deleted = await ctx.channel.purge(limit=number)
	print('Deleted {} message(s)'.format(len(deleted)))
	logger.info('Deleted {} message(s)'.format(len(deleted)))
	await ctx.send("Deleted {} messages, my master.".format(len(deleted)))
@bot.command(pass_context=True)
async def getimage(ctx, *, image):
	"""Tests downloading - owner only"""
	
	mess = await Message.Embed(title="Test", description="Downloading file...").send(ctx)
	file_path = await GetImage.download(image)
	mess = await Message.Embed(title="Test", description="Uploading file...").edit(ctx, mess)
	await Message.EmbedText(title="Image", file=file_path).edit(ctx, mess)
	GetImage.remove(file_path)

@bot.command(aliases=["askmeanything", "ass.com"])
async def ask(ctx, *, query = None):
	"""Jeeves, please answer these questions."""

	if query == None:
		msg = 'You need a topic for me to Ask Jeeves.'
		await ctx.send(msg)
		return

	msg = await get_search(ctx, query,"k")
	# Say message
	await ctx.send(msg)

@bot.command()
@has_permissions(manage_messages=True)
async def purgeall(ctx):
	"""Deletes all messages in a channel"""
	await ctx.trigger_typing()
	await ctx.channel.purge(limit=None, check=lambda message: not message.pinned)
	await ctx.send("I have successfully cleared everything in this channel!")
@bot.command()
async def hello(ctx):
	"""Says hello to a person"""
	response = f"Hello {ctx.author.mention}"
	response = str(response)
	await ctx.send(response)
	print (f"Said hello to {ctx.author}.")  
@bot.command()
async def goodmorning(ctx):
	"""It's a good morning"""
	await ctx.send(f"Good Morning, {ctx.author.mention}!")
@bot.command(aliases=["makebig", "enlargen", "supersize"])
async def embiggen(ctx, *, text):
	"""Embiggens text. Yes that's a word, obviously"""
	await ctx.send("```fix\n" + figlet_format(text, font="big") + "```")
@bot.command(pass_context=True)
async def duck(ctx, *, query = None):
	"""Duck Duck... GOOSE."""

	if query == None:
		msg = 'You need a topic for me to DuckDuckGo.'
		await ctx.send(msg)
		return

	msg = await get_search(ctx, query,"d")
	# Say message
	await ctx.send(msg)
@bot.command()
async def terrariaquotes(ctx):
	terrariaquote = open("terrariaquotes.py").read().splitlines()
	terraria = random.choice(terrariaquote)
	await ctx.send(terraria)
@bot.command(aliases=["makemelaugh", "memes", "funnies"])
async def meme(ctx):
	"""MEMES BOII"""
	await ctx.send("Here we go! Here comes a meme!")
	await ctx.send(random.choice(memes))

@bot.command()
async def highfive(ctx):
	"""Some people just need a highfive..."""
	await ctx.send(":hand_splayed:" + " " + "You've been highfived.")

@bot.command()
async def moveout(ctx):
	"""How long until I can finally leave my parents"""
	await ctx.send("**{0}** day(s) left until I FINALLY  move out!! :smile:".format(str(moveoutday.days)))
@bot.command(aliases=["xmas", "chrimbo", "crimbo", "Christmas"])
async def christmas(ctx):
	"""HOW MUCH LONGER TILL CHRISTMAS, MOMMY?!?!"""
	await ctx.send("**{0}** day(s) left until Christmas day! :christmas_tree:".format(str(diff.days)))
@bot.command(aliases=["ud", "urbandict", "define"])
async def urban(ctx, *msg):
	"""Define stuff with Urban Dict"""
	print("hi")
	word = ' '.join(msg)
	api = "http://api.urbandictionary.com/v0/define"
	logger.info("Making request to " + api)
	# Send request to the Urban Dictionary API and grab info
	response = requests.get(api, params=[("term", word)]).json()
	embed = discord.Embed(description="No results found!", colour=0xFF0000)
	if len(response["list"]) == 0:
		return await ctx.send(embed=embed)
	# Add results to the embed
	embed = discord.Embed(title="Word", description=word, colour=embed.colour)
	embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
	embed.add_field(name="Examples:", value=response['list'][0]['example'])
	await ctx.send(embed=embed)
@bot.command(aliases=["aboutguild", "aboutserver", "serverinfo"])
async def guildinfo(ctx):
	"""About the guild"""
	guild = ctx.guild
	total_text_channels = len(guild.text_channels)
	total_voice_channels = len(guild.voice_channels)
	total_channels = total_text_channels  + total_voice_channels 
	embed = discord.Embed(title="guild Info: " + str(guild.name), color=0xff00ae)
	embed2 = discord.Embed(title="guild Info Continued: " + str(guild.name), color=0xff00ae)
	embed3 = discord.Embed(title="More guild Info: ", color=0xff00ae)
	embed2.add_field(name="2fa level: ", value=guild.mfa_level)
	embed2.add_field(name="Verification: ", value=guild.verification_level)
	embed.add_field(name="Icon: ", value=guild.icon)
	embed.add_field(name="Icon URL", value=guild.icon_url)
	embed.add_field(name="ID: ", value=guild.id)
	embed2.add_field(name="Emojis", value=len(guild.emojis))
	embed.add_field(name="Icon animated", value=guild.is_icon_animated())
	embed2.add_field(name="System Channel", value=guild.system_channel)
	embed2.add_field(name="Rules Channel", value=guild.rules_channel)
	embed2.add_field(name="AFK Timeout", value=guild.afk_timeout)
	embed2.add_field(name="AFK Channel", value=guild.afk_channel)
	embed2.add_field(name="Region: ", value=guild.region)
	embed2.add_field(name="# of roles", value=len(guild.roles))
	embed2.add_field(name="Notify Settings: ", value=guild.default_notifications)
	embed.add_field(name="Owner's ID: ", value=guild.owner)
	embed.add_field(name="Max Members: ", value=guild.max_members)
	embed.add_field(name="Banner: ", value=guild.banner)
	embed2.add_field(name="Filter", value=guild.explicit_content_filter)
	embed2.add_field(name="Server Channels: ", value=total_channels )
	embed2.add_field(name="Server Text Channels: ", value=total_text_channels)
	embed2.add_field(name="Server Voice Channels: ", value=total_voice_channels)
	embed.add_field(name="Description: ", value=guild.description)
	embed2.add_field(name="Splash: ", value=guild.splash)
	embed.add_field(name="How many boosters? ", value=guild.premium_subscription_count)
	embed2.add_field(name="Max # of Emojis: ", value=guild.emoji_limit)
	embed.add_field(name="Filesize: ", value=guild.filesize_limit)
	embed.add_field(name="# of Members: ", value=guild.member_count)
	embed.add_field(name="Created at: ", value=guild.created_at)
	await ctx.send(embed=embed)
	await ctx.send(embed=embed2)
@bot.command(aliases=["nickchange", "changenick"])
async def changenickname(ctx, member : discord.Member, *, message):
	"""Change a user's nickname"""
	await member.edit(nick=message)
	await ctx.send(f"Success! {member}'s Nickname changed to {message}")
@bot.command(aliases=["aboutuser", "memberinfo"])
async def userinfo(ctx, member : discord.Member):
	"""Info about user"""
	embed = discord.Embed(title="User Info", color=0xff00ae)
	embed.add_field(name="Name: ", value=member.name)
	embed.add_field(name="web status", value=member.web_status)
	embed.add_field(name="On Mobile? ", value=member.is_on_mobile())
	embed.add_field(name="Status: ", value=member.status)
	embed.add_field(name="Desktop Status: ", value=member.desktop_status)
	embed.add_field(name="roles: ", value=member.roles)
	embed.add_field(name='Joined this Server: ', value=member.joined_at)
	embed.add_field(name='Nickname', value=member.nick)
	embed.add_field(name="Highest Role: ", value=member.top_role)
	embed.add_field(name="Avatar: ", value=member.avatar)
	embed.add_field(name="Avatar URL: ", value=member.avatar_url)
	embed.add_field(name="Created At: ", value=member.created_at)
	embed.add_field(name="Discriminator: ", value=member.discriminator)
	embed.add_field(name="Bot?", value=member.bot)
	embed.add_field(name="ID: ", value=member.id)
	#embed.add_field(name="Name: ", value=member.name)
	await ctx.send(embed=embed)
@bot.command()
async def backwards(ctx, *, message):
	"""Sends a message backwards"""
	await ctx.send(message[::-1])
@bot.command()
async def areyoutired(ctx):
	"""Is the bot tired?"""
	yes = "yes"
	no = "no"
	await ctx.send(random.choice([yes, no]))
@bot.command()
async def timetravel(ctx, message):
	"""Just don't mess up the timeline..."""
	await ctx.send(f"skipping forward {message} minutes")
	await ctx.message.delete()
@bot.command()
async def clock(ctx):
	"""What time is it?"""
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	await ctx.send(f"now = {current_time}")
@bot.command()
async def recentjoins(ctx):
	"""Lists the most recent users to join."""
	our_list = []
	# offset = settings.getGlobalUserStat(ctx.author,"TimeZone",settings.getGlobalUserStat(ctx.author,"UTCOffset",None))
	for member in ctx.guild.members:
		our_list.append(
			{
				"name":member.name,
				"value":"{} UTC".format(member.joined_at.strftime("%Y-%m-%d %I:%M %p") if member.joined_at != None else "Unknown"),#UserTime.getUserTime(ctx.author,self.settings,member.joined_at,force=offset)["vanity"],
				"date":member.joined_at
			}
		)
	our_list = sorted(our_list, key=lambda x:x["date"].timestamp() if x["date"] != None else -1)
	return await PickList.PagePicker(title="Most Recent Members to Join {} ({:,} total)".format(ctx.guild.name,len(ctx.guild.members)),ctx=ctx,list=[{"name":"{}. {}".format(y+1,x["name"]),"value":x["value"]} for y,x in enumerate(our_list)]).pick()
 
@bot.command()
async def google(ctx, *, query = None):
	"""Get some searching done."""

	if query == None:
		msg = 'You need a topic for me to Google.'
		await ctx.send(msg)
		return

	msg = await get_search(ctx, query)
	# Say message
	await ctx.send(msg)
@bot.command(name="spam2.0")
async def spam2point0(ctx, *, message):
	"""Spams a message"""
	await ctx.send("usage = %spam2.0 <message>")
	if message == "@everyone":
		ctx.send("No")
	x = 1
	while x < 12:
		await ctx.send(message)
		x += 1
		if x == 13:
			break

@bot.command(pass_context=True)
async def bing(ctx, *, query = None):
	"""Get some uh... more searching done."""

	if query == None:
		msg = 'You need a topic for me to Bing.'
		await ctx.channel.send(msg)
		return

	msg = await get_search(ctx, query,"b")
	# Say message
	await ctx.channel.send(msg)
@bot.command()
async def speedstest(ctx):
	"""Internet Speedtest"""
	message = await ctx.send('Running speed test...')
	try:
		st = speedtest.Speedtest()
		st.get_best_server()
		l = asyncio.get_event_loop()
		msg = '**Speed Test Results:**\n'
		msg += '```\n'
		await message.edit(content="Running speed test...\n- Downloading...")
		a = bot.loop.run_in_executor(None, st.download)
		d = await a
		msg += 'Download: {}Mb/s\n'.format(round(d/1024/1024, 2))
		await message.edit(content="Running speed test...\n- Downloading...\n- Uploading...")
		a = bot.loop.run_in_executor(None, st.upload)
		u = await a
		msg += '  Upload: {}Mb/s```'.format(round(u/1024/1024, 2))
		await message.edit(content=msg)
	except Exception as e:
		await message.edit(content="Speedtest Error: {}".format(str(e)))
@bot.command()
async def claptrap(ctx):
	"""Can I shoot something now? SOMETHING exciting?"""
	claptraps = open("claptraps.py", encoding="utf8").read().splitlines()
	claptrap = random.choice(claptraps)
	await ctx.send(claptrap)
@bot.command(pass_context=True)
async def hostinfo(ctx):
	"""Info about the bot's host environment."""

	message = await ctx.channel.send('Gathering info...')

	# cpuCores    = psutil.cpu_count(logical=False)
	# cpuThred    = psutil.cpu_count()
	cpuThred      = os.cpu_count()
	cpuUsage      = psutil.cpu_percent(interval=1)
	memStats      = psutil.virtual_memory()
	memPerc       = memStats.percent
	memUsed       = memStats.used
	memTotal      = memStats.total
	memUsedGB     = "{0:.1f}".format(((memUsed / 1024) / 1024) / 1024)
	memTotalGB    = "{0:.1f}".format(((memTotal/1024)/1024)/1024)
	currentOS     = platform.platform()
	system        = platform.system()
	release       = platform.release()
	version       = platform.version()
	processor     = platform.processor()
	botName       = "Terrabot"
	currentTime   = int(time.time())
	timeString    = ReadableTime.getReadableTimeBetween(startTime, currentTime)
	pythonMajor   = sys.version_info.major
	pythonMinor   = sys.version_info.minor
	pythonMicro   = sys.version_info.micro
	pythonRelease = sys.version_info.releaselevel
	pyBit         = struct.calcsize("P") * 8

	threadString = 'thread'
	if not cpuThred == 1:
		threadString += 's'

	msg = '***{}\'s*** **Home:**\n'.format(botName)
	msg += '```\n'
	msg += 'OS       : {}\n'.format(currentOS)
	msg += 'Hostname : {}\n'.format(platform.node())
	msg += 'Language : Python {}.{}.{} {} (64 bit)\n'.format(pythonMajor, pythonMinor, pythonMicro, pythonRelease, pyBit)
	msg += 'Commit   : "idkthispreventserror"'
	msg += ProgressBar.center('{}% of {} {}'.format(cpuUsage, cpuThred, threadString), 'CPU') + '\n'
	msg += ProgressBar.makeBar(int(cpuUsage)) + "\n\n"
	msg += ProgressBar.center('{} ({}%) of {}GB used'.format(memUsedGB, memPerc, memTotalGB), 'RAM') + '\n'
	msg += ProgressBar.makeBar(int(memPerc)) + "\n\n"
	msg += '{} uptime```'.format(timeString)

	await message.edit(content=msg)
@bot.command()
async def turret(ctx):
		"""Now you're thinking with - wait... turrets?"""
		turrets = open("turrets.py").read().splitlines()
		await ctx.send(random.choice(turrets))
@bot.command()
async def spam(ctx, member:discord.Member):
	"""Spam pings a user"""
	x = 1
	while x < 16:
		await ctx.send(f"{member.mention}")
		x+=1
		if x == 17:
			break
@bot.command()
async def swear(ctx):
	await ctx.send("Fuckin fuck shit bich!")
	await asyncio.sleep(5)
	await ctx.send(":disappointed:")
	await asyncio.sleep(5)
	await ctx.send("I'm so sorry. I don't know what came over me.")
@bot.command()
@commands.is_owner()
async def announce(ctx, member : discord.Member, *message:str):
	"""Announces stuff to whoever is pinged"""
	await ctx.send(message)
@bot.command()
@has_permissions(embed_links=True)
async def Reeeeee(ctx):
	"""REEEEEEE!"""
	await ctx.send("https://www.youtube.com/watch?v=m4-IWUfddOE")
@bot.command()
async def delrole(ctx, role:discord.Role):
	await Role.delete(role, reason=None)
	embed = discord.Embed(title="Role Deleted", description="Deleted the role {}".format(role.name), color=0xff00ae)
	embed.set_footer(text="Powered by Terrabot")
	await ctx.send(embed=embed)
@bot.command()
@has_permissions(manage_emojis=True)
async def createemoji(ctx):
	guild = ctx.guild
	image = open("4_grande.png", encoding='utf-8')
	image.read()
	await guild.create_custom_emoji(name="celebration", image=image)
@bot.command()
async def beer(ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
		""" Give someone a beer! 🍻 """
		if not user or user.id == ctx.author.id:
			return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
		if user.id == bot.user.id:
			return await ctx.send("*drinks beer with you* 🍻")
		if user.bot:
			return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

		beer_offer = f"**{user.mention}**, you got a 🍺 offer from **{ctx.author.name}**"
		beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
		msg = await ctx.send(beer_offer)

		def reaction_check(m):
			if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
				return True
			return False

		try:
			await msg.add_reaction("🍻")
			await bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
			await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
		except asyncio.TimeoutError:
			await msg.delete()
			await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
		except discord.Forbidden:
			# Yeah so, bot doesn't have reaction permission, drop the "offer" word
			beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
			beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
			await msg.edit(content=beer_offer)
@bot.command()
async def heal(ctx, member:discord.Member):
	await ctx.send(f"Attempting to heal {member.mention}")
	await asyncio.sleep(3)
	options = ["Healing Failed", "Yay! It worked!"]
	await ctx.send(random.choice(options))
@bot.command()
async def feed(ctx, member:discord.Member, *food):
	await ctx.send("Fed {} {}".format(member, food))

token = 
bot.run(token)