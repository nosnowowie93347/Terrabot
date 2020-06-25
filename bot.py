import discord, re, traceback, aiohttp, platform, sqlite3, asyncio, psutil, time, requests, urllib.request, logging, json, typing, random, os, psutil, platform, time, sys, fnmatch, subprocess, speedtest, json, struct
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
from utils.tools import *
from utils.channel_logger import Channel_Logger
from discord.utils import get
from utils.language import Language
from   discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions, bot_has_permissions
import datetime
from utils import checks
import pyfiglet, time
from pyfiglet import figlet_format, FontNotFound
import datetime as dt
from utils.logger import log
lock_status = config.lock_status
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
bot = discord.ext.commands.Bot(command_prefix=config.command_prefixes, case_insensitive=True, description="Hello my name is Terrabot")
channel_logger = Channel_Logger(bot)
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
EMOJI_NAME_REGEX = re.compile(r"<a?(:\w{2,32}:)\d{15,}>")
client = discord.Client()
today = datetime.date.today()
now = datetime.datetime.now()
conn = sqlite3.connect("data/Ruby.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
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
limit = config.max_nsfw_count
rockpaperscissors = random.choice(choices)
random_word = random.choice("words.txt")
lines = open('words.txt').read().splitlines()
startTime = int(time.time())
compliments = open("Compliments.txt", encoding='utf8').read().splitlines()
myline = random.choice(lines)
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
	bot.load_extension("invite")
	bot.load_extension("emojis")
	bot.load_extension("muusic")
	bot.load_extension("quickpoll")
	bot.load_extension("Morecogs")
	bot.load_extension("Morse")
	bot.load_extension("Botstuff")
	bot.load_extension("Admin")
	bot.load_extension("Translate")
	bot.load_extension("cogs4")
	await bot.change_presence(activity=discord.Game(name="Serving Pinkalicious21902 Forever and Always"), status=discord.Status.online)
	print(time.time())
	print(len(bot.commands))

@bot.event
async def on_message(message):
		# swearwords = ["shit", "cock", "porn", "dick", "slut", "pussy", "bitch", "cunt", "fuck", "fag", "bastard", "sex", "retard", "vagina"]
	# for word in swearwords:
	# 	if word in message.content:
	# 		await message.delete()
	# 		await message.channel.send("Hey! watch the language")
			

	# if message.content.startswith("how dare u disrespect your master"):
	# 	await message.channel.send("I'm NOT sorry")
	# if message.content.startswith("x&"):
	# 	await message.delete(delay=None)
	# 	embed=discord.Embed(title="Nice try. Ruby's been blocked")
	# 	await message.channel.send(embed=embed)
	# 	await message.channel.send("You block mine, I block urs. From Pink.")
	if message.author.bot:
		return
	await bot.process_commands(message)
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Oops! This command doesn't exist. If you think it should, dm the devs with ur suggestion.")
		return
	if isinstance(error, commands.DisabledCommand):
		await ctx.send(Language.get("bot.errors.disabled_command", ctx))
		return
	if isinstance(error, checks.owner_only):
		await ctx.send(Language.get("bot.errors.owner_only", ctx))
		return
	if isinstance(error, checks.dev_only):
		await ctx.send(Language.get("bot.errors.dev_only", ctx))
		return
	if isinstance(error, checks.support_only):
		await ctx.send(Language.get("bot.errors.support_only", ctx))
		return
	if isinstance(error, checks.not_nsfw_channel):
		await ctx.send(Language.get("bot.errors.not_nsfw_channel", ctx))
		return
	if isinstance(error, checks.not_guild_owner):
		await ctx.send(Language.get("bot.errors.not_guild_owner", ctx))
		return
	if isinstance(error, checks.no_permission):
		await ctx.send(Language.get("bot.errors.no_permission", ctx))
		return
	if isinstance(error, commands.NoPrivateMessage):
		await ctx.send(Language.get("bot.errors.no_private_message", ctx))
		return
	if isinstance(ctx.channel, discord.DMChannel):
		await ctx.send(Language.get("bot.errors.command_error_dm_channel", ctx))
		return

	#In case the bot failed to send a message to the channel, the try except pass statement is to prevent another error
	try:
		await ctx.send(Language.get("bot.errors.command_error", ctx).format(error))
	except:
		pass
	log.error("An error occured while executing the {} command: {}".format(ctx.command.qualified_name, error))
@bot.event
async def on_member_join(user): 
	try:
		rules = discord.Embed(title="Rules", description="These are the rules", color=0xff00ae)
		rules.add_field(name="1", value="Leave banning the bots to Devs/admins")
		rules.add_field(name="2", value="Behave/use common sense")
		rules.add_field(name="3", value="#mute-appeal for unfair mutes")
		rules.add_field(name="4", value="Admins and maybe staff will purge channels. see #purge-notices")
		await user.send(embed=rules)
	except discord.errors.Forbidden:
		return
@bot.event
async def on_reaction_add(reaction, user):
		bot.dispatch("picklist_reaction", reaction, user)



def blacklistuser(id, name, discrim, reason):
	cur.execute("""INSERT INTO blacklist(id, name, discrim, reason) VALUES (?, ?, ?, ?)""", (id, name, discrim, reason))
	conn.commit()

def unblacklistuser(id):
	cur.execute("""DELETE FROM blacklist WHERE id=""" + str(id))
	conn.commit()

def getblacklistentry(id):
	cur.execute("""SELECT id FROM blacklist WHERE id=""" + str(id))
	id = None
	name = None
	discrim = None
	reason = None
	try:
		id = cur.fetchone()[0]
	except:
		return None
	cur.execute("""SELECT name FROM blacklist WHERE id=""" + str(id))
	name = cur.fetchone()[0]
	cur.execute("""SELECT discrim FROM blacklist WHERE id=""" + str(id))
	discrim = cur.fetchone()[0]
	cur.execute("""SELECT reason FROM blacklist WHERE id=""" + str(id))
	reason = cur.fetchone()[0]
	blacklistentry = {"id":id, "name":name, "discrim":discrim, "reason":reason}
	return blacklistentry

def getblacklist():
	cur.execute("""SELECT id, name, discrim, reason FROM blacklist""")
	entries = []
	rows = cur.fetchall()
	for row in rows:
		entry = "ID: \"{}\" Name: \"{}\" Discrim: \"{}\" Reason: \"{}\"".format(row["id"], row["name"], row["discrim"], row["reason"])
		entries.append(entry)
	return entries

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

@bot.command(aliases=["wipe", "delete", "clean", "removespam"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number: int):
	"""Deletes a certain number of messages"""
	await ctx.trigger_typing()
	deleted = await ctx.channel.purge(limit=number)
	print('Deleted {} message(s)'.format(len(deleted)))
	logger.info('Deleted {} message(s)'.format(len(deleted)))
	await ctx.send("Deleted {} messages, my master.".format(len(deleted)), delete_after=5)
@bot.command(pass_context=True)
async def getimage(ctx, *, image):
	"""Tests downloading - owner only"""
	
	mess = await Message.Embed(title="Test", description="Downloading file...").send(ctx)
	file_path = await GetImage.download(image)
	mess = await Message.Embed(title="Test", description="Uploading file...").edit(ctx, mess)
	await Message.EmbedText(title="Image", file=file_path).edit(ctx, mess)
	GetImage.remove(file_path)

@bot.command()
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
@checks.is_dev()
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
@bot.command()
async def highfive(ctx):
	"""Some people just need a highfive..."""
	await ctx.send(":hand_splayed:" + " " + "You've been highfived.")

@bot.command()
async def moveout(ctx):
	"""How long until I can finally leave my parents"""
	await ctx.send("**{0}** day(s) left until I FINALLY  move out!! :smile:".format(str(moveoutday.days)))
@bot.command(aliases=["xmas", "chrimbo", "crimbo"])
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
	categories = len(guild.categories)
	total_channels = total_text_channels  + total_voice_channels 
	embed = discord.Embed(title="guild Info: " + str(guild.name), color=0xff00ae)
	embed2 = discord.Embed(title="guild Info Continued: " + str(guild.name), color=0xff00ae)
	embed3 = discord.Embed(title="More guild Info: ", color=0xff00ae)
	embed2.add_field(name="2fa level: ", value=guild.mfa_level)
	embed2.add_field(name="Verification: ", value=guild.verification_level)
	embed2.add_field(name="Emojis", value=len(guild.emojis))
	embed.add_field(name="Icon:", value=guild.icon)
	embed.add_field(name="Total text channels:", value=total_text_channels)
	embed.add_field(name="Total voice channels:", value=total_voice_channels)
	embed.add_field(name="Total channels:", value=total_channels)
	embed.add_field(name="# of categories:", value=categories)
	embed.add_field(name="This guild is large", value=guild.large)
	embed.add_field(name="Icon animated", value=guild.is_icon_animated())
	embed2.add_field(name="System Channel", value=guild.system_channel)
	embed2.add_field(name="Rules Channel", value=guild.rules_channel)
	embed2.add_field(name="AFK Timeout", value=guild.afk_timeout)
	embed2.add_field(name="AFK Channel", value=guild.afk_channel)
	embed2.add_field(name="Region: ", value=guild.region)
	embed2.add_field(name="# of roles", value=len(guild.roles))
	embed2.add_field(name="Notify Settings: ", value=guild.default_notifications)
	embed2.add_field(name="Filter", value=guild.explicit_content_filter)
	embed2.add_field(name="Max # of Emojis: ", value=guild.emoji_limit)
	embed.add_field(name="# of Members: ", value=guild.member_count)
	embed.add_field(name="Created at: ", value=guild.created_at)
	await ctx.send(embed=embed)
	await ctx.send(embed=embed2)
@bot.command()
async def botserver(ctx):
	"""Sends an invite link to the bot's server"""
	await ctx.send(Language.get("bot.invite", ctx).format("https://discord.gg/MJsmbD2", bot.command_prefix))
	await ctx.author.send(Language.get("bot.invite", ctx).format("https://discord.gg/MJsmbD2", bot.command_prefix))
@bot.command()
async def oeis(ctx, *, number: str):
	'''
	Looks up a sequence of numbers
	'''
	req=requests.get('https://oeis.org/search?q={}&fmt=json'.format(number)).json()['results'][0]
	numid = 'A'+str(req['number']).zfill(6)
	embed = discord.Embed(title='**'+numid+'**', url='https://oeis.org/{}'.format(numid), description='**'+req['name']+'**', color=0xFF0000)
	embed.add_field(name="Numbers:", value=str(req['data']), inline=False)
	embed.set_image(url='https://oeis.org/{}/graph?png=1'.format(numid))
	embed.set_thumbnail(url='https://oeis.org/oeis_logo.png')
	embed.set_footer(text='OEIS', icon_url='https://oeis.org/oeis_logo.png')
	embed.set_author(name='OEIS.org', url='https://oeis.org/', icon_url='https://oeis.org/oeis_logo.png')
	embed.timestamp = datetime.datetime.utcnow()
	await ctx.send('**Search result for:** ***{}...***'.format(number), embed=embed)
@bot.command()
async def online(ctx):
	# Set the filter to be a non-offline member, and the member not being a bot.
	def filterOnlyOnlineMembers(member):
		return member.status != discord.Status.offline
	membersInServer = ctx.guild.members
	onlineMembersInServer = list(filter(filterOnlyOnlineMembers, membersInServer))
	onlineMembersCount = len(onlineMembersInServer)
	await ctx.send("There are " + str(onlineMembersCount) + " Members online out of {}".format(len(ctx.guild.members)))
@bot.command()
async def kill(ctx, member:discord.Member):
	'''
	Kills the player, minecraft style
	'''
	causeofdeath = ["fell out of the world", "watched their innards become outards", "forgot to breath", "watched their legs appear where their head should be", "hit the ground too hard", "was shot by skeleton"]
	await ctx.send("{}".format(member.mention))
	await ctx.send(random.choice(causeofdeath))
@bot.command(aliases=["nickchange", "changenick"])
@has_permissions(manage_nicknames=True)
async def changenickname(ctx, member : discord.Member, *, message):
	"""Change a user's nickname"""
	await member.edit(nick=message)
	await ctx.send(f"Success! {member}'s Nickname changed to {message}")
@bot.command()
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
	embed.add_field(name="Current Activities", value=member.activities)
	embed.add_field(name="Mentionable String", value=member.mention)

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
async def timetravel(ctx, numofminutes:int):
	"""Just don't mess up the timeline..."""
	await ctx.send(f"skipping forward {numofminutes} minutes", delete_after=35)
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
@bot.command(name="spam2.0", enabled=False, hidden=True)
@checks.is_owner()
async def spam2point0(ctx, *, message):
	"""Spams a message"""
	await ctx.send("usage = %spam2.0 <message>")
	if message == "@everyone":
		return await ctx.send("No")
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
@bot.command(name="speedtest")
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
@bot.command(aliases=["getprefix", "botprefix"])
async def prefix(ctx):
	message = discord.Message
	prefix = await bot.get_prefix(message)
	await ctx.send(f"My prefixes are {prefix}.")
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
@bot.command(enabled=False, hidden=True)
@checks.is_dev()
async def spam(ctx, member:discord.Member):
	"""Spam pings a user"""
	x = 1
	while x < 16:
		await ctx.send(f"{member.mention}")
		x+=1
		if x == 17:
			break
@bot.command()
@has_permissions(embed_links=True)
async def Reeeeee(ctx):
	"""REEEEEEE!"""
	await ctx.send("https://www.youtube.com/watch?v=m4-IWUfddOE")

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
@bot.command(aliases=["b&w"])
async def blackandwhite(ctx, user:discord.Member=None):
	"""Turns your avatar or the specified user's avatar black and white"""
	await ctx.channel.trigger_typing()
	if user is None:
		user = ctx.author
	download_file(get_avatar(user, animate=False), "data/blackandwhite.png")
	avatar = Image.open("data/blackandwhite.png").convert("L")
	avatar.save("data/blackandwhite.png")
	await ctx.send(file=discord.File("data/blackandwhite.png"))
@bot.command()
async def f(ctx):
	"""Press F to pay your respects"""
	await ctx.send(Language.get("fun.respects", ctx).format(ctx.author, random.randint(1, 10000)))
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
	userAvatarUrl = avamember.avatar_url
	await ctx.send(userAvatarUrl)
@bot.command()
async def uploadfile(ctx, *, path:str):
	"""Uploads any file on the system. What is this hackery?"""
	await ctx.channel.trigger_typing()
	try:
		await ctx.send(file=discord.File(path))
	except FileNotFoundError:
		await ctx.send("That file does not exist!")
@bot.command(name="pi")
async def calculatepi(ctx, n:int):
	def roundpi(n):
		return round(math.pi, n)
	if n > 15:
		return await ctx.send("the maximum is 15 digits sadly.")
	await ctx.send(roundpi(n))
@bot.command()
@commands.is_nsfw()
async def rule34(ctx, *, tags:str):
	await ctx.channel.trigger_typing()
	try:
		data = requests.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(limit, tags), headers=header).json()
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
		image = data[random.randint(0, count)]
		images.append("http://img.rule34.xxx/images/{}/{}".format(image["directory"], image["image"]))
	await ctx.send(Language.get("nsfw.results", ctx).format(image_count, count, tags, "\n".join(images)))

@bot.command(aliases=["cutedog", "randomdog"])
async def shibe(ctx):
	"""Sends a random shibe picture."""
	try:
		image = requests.get("http://shibe.online/api/shibes?count=1&urls=true").json()
		print(image[0])
		
		embed = discord.Embed()
		embed.set_image(url=image[0])
		await ctx.send(embed=embed)
		
	except aiohttp.ClientError:
		await ctx.send(f"{ctx.tick(False)} Failed to grab a shibe. Try again later.")

@bot.command(name="emojinames")
@commands.guild_only()
@commands.has_permissions(read_message_history=True)
async def namesofemojis(ctx):
	from typing import Set
	import functools
	"""Shows the names of recent custom emoji used.
	Useful for mobile users.
	"""

	def reducer(emoji: Set[str], message: discord.Message):
		names = EMOJI_NAME_REGEX.findall(message.content)
		return emoji | set(names)

	messages = await ctx.history(limit=50).flatten()
	names: Set[str] = functools.reduce(reducer, messages, set())

	if not names:
		await ctx.send("No recently used custom emoji were found.")
	else:
		formatted = ", ".join(f"`{name}`" for name in names)
		await ctx.send(formatted)
@bot.command()
async def quoteaf(ctx):
	"""Don't quote me on that"""
	await ctx.channel.trigger_typing()
	await ctx.send(file=discord.File("assets/imgs/quotes/{}.png".format(random.randint(1, len([file for file in os.listdir("assets/imgs/quotes")])))))		
@bot.command()
async def ron(ctx):
	"""Get a Ron Swanson quote"""
	req = requests.get("https://ron-swanson-quotes.herokuapp.com/v2/quotes")
	quote = req.json()
	await ctx.send(quote[0])
@bot.command(aliases=["memes", "memey", "memer"])
async def meme(ctx):
	embed = discord.Embed(title="Meme", description="Here comes a meme!!")
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)
@bot.command()
async def choose(ctx, *, text: str):
	"""Choose between options (seperated by commas)"""
	# Remove spaces and white space, split into a list and choose a random element
	text = text.strip()
	temp = text.split(",")
	await ctx.send("I choose... **{}** :thinking:".format(temp[random.randint(0, len(temp) - 1)]))

@bot.command(aliases=["change_stream"])
async def stream(ctx, *, name:str):
	"""Sets the streaming status with the specified name"""
	if lock_status:
		if not ctx.author.id == config.owner_id and not ctx.author.id in config.dev_ids:
			await ctx.send(Language.get("bot.status_locked", ctx))
			return
	await bot.change_presence(activity=discord.Activity(name=name, type=discord.ActivityType.streaming, url="https://www.twitch.tv/ZeroEpoch1969"))
	await ctx.send(Language.get("bot.now_streaming", ctx).format(name))
	await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the streaming status to `{}`".format(ctx.author.id, ctx.author, name))
@bot.command()
async def inviteme(ctx):
	"""Sends the bot's OAuth2 link"""
	await ctx.send(Language.get("bot.joinserver", ctx).format("https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927"))
	await ctx.author.send(Language.get("bot.joinserver", ctx).format("https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927"))
@bot.command()
async def suggest(ctx, *, suggestion:str):
	"""Sends a suggestion to the developers"""
	if isinstance(ctx.channel, discord.DMChannel):
		guild = "`No server! Sent via Private Message!`"
	else:
		guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
	msg = make_message_embed(ctx.author, 0xFF0000, suggestion, formatUser=True)
	owner = bot.get_user(config.owner_id)
	if owner:
		await owner.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
	for id in config.dev_ids:
		dev = bot.get_user(id)
		if dev:
			await dev.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
@bot.command(hidden=True)
async def botserverids(ctx):
	await ctx.send(bot.guilds)
	await ctx.send(len(bot.guilds))
@bot.command(hidden=True)
@commands.is_owner()
async def delguild(ctx, guild_id):
	guildtodelete = await bot.fetch_guild(guild_id)
	await guildtodelete.delete()
	await ctx.send(f"The guild {guild_id} was successfully deleted.")
@bot.command(aliases=["report", "notifydevs"])
async def notifydev(ctx, *, message:str):
	"""Sends a message to the developers"""
	if isinstance(ctx.channel, discord.DMChannel):
		guild = "`No server! Sent via Private Message!`"
	else:
		guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
	msg = make_message_embed(ctx.author, 0xFF0000, message, formatUser=True)
	owner = bot.get_user(config.owner_id)
	if owner:
		await owner.send("You have received a new message! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
	for id in config.dev_ids:
		dev = bot.get_user(id)
		if dev:
			await dev.send("You have received a new message! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
	
	await ctx.author.send(Language.get("bot.dev_notify", ctx).format(message))
@bot.command(hidden=True, aliases=["createguild", "create_guild"])
@commands.is_owner()
async def hopethisworks(ctx, name):
	# VoiceRegion = ctx.guild.region
	with open('AwOo.png', 'rb') as f:
		icon = f.read()
	print("Here!")
	newserver = await bot.create_guild(name=name, region=VoiceRegion.us_west, icon=icon)
	await newserver.create_text_channel(name="whatever")
	invite = await newserver.channels[0].create_invite()
	await ctx.send(invite)
	print("And Here!")

token = ""
bot.run(token)