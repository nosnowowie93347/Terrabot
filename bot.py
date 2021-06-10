import math, datetime, time, pendulum, aiohttp, sqlite3, asyncio, logging, os, platform, json, textwrap
from PIL import Image
from pathlib import Path
from discord.ext import commands
import discord.utils
import motor.motor_asyncio
import utils.json_loader
from utils.tools import *
from utils.mongo import Document
from utils.channel_logger import Channel_Logger
from utils.language import Language
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions, bot_has_permissions
from utils import config
from pyfiglet import figlet_format
from discord import Spotify
from dotenv import load_dotenv


async def get_prefix(bot, message):
	try:
		data = await bot.config.find(message.guild.id)

		# Make sure we have a useable prefix
		if not data or "prefix" not in data:
			return commands.when_mentioned_or(config.command_prefixes)(bot, message)
		return commands.when_mentioned_or(data["prefix"])(bot, message)
	except:
		return commands.when_mentioned_or(config.command_prefixes)(bot, message)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logfile = 'discord.txt'
intents = discord.Intents.all()
bot = discord.ext.commands.Bot(help_command=None, command_prefix=get_prefix, intents=intents, case_insensitive=True, description="Hello my name is Terrabot. I'm made by Pinkalicious21902", owner_ids=[466778567905116170, 735237182649794571])
channel_logger = Channel_Logger(bot)
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

EMOJI_NAME_REGEX = re.compile(r"<a?(:\w{2,32}:)\d{15,}>")
client = discord.Client()
today = datetime.date.today()
bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.connection_url = config.connection_url
bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
bot.db = bot.mongo["pinkalicious"]
bot.reaction_roles = Document(bot.db, "reaction_roles")
bot.muted_users = {}
bot.mutes = Document(bot.db, "mutes")
bot.warns = Document(bot.db, "warns")
bot.command_usage = Document(bot.db, "command_usage")
bot.config = Document(bot.db, "config")
bot.reaction_roles = Document(bot.db, "reaction_roles")
bot.color_list = [c for c in bot.colors.values()]
now = datetime.datetime.now()
conn = sqlite3.connect("data/Ruby.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
suggestionsssss = []
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
choices = ['rock', 'paper', 'scissors']
cwd = Path(__file__).parents[0]
cwd = str(cwd)
limit = config.max_nsfw_count
rockpaperscissors = random.choice(choices)
random_word = random.choice("words.txt")
lines = open('words.txt').read().splitlines()
startTime = int(time.time())
compliments = open("Compliments.txt", encoding='utf8').read().splitlines()
myline = random.choice(lines)
bot.blacklisted_users = []
cwd = Path(__file__).parents[0]
cwd = str(cwd)
bot.cwd = cwd
cogdir = f"{cwd}/cogs"

@bot.event
async def on_ready():
	print(cwd)
	data = utils.json_loader.read_json("blacklist")
	bot.blacklisted_users = data["blacklistedUsers"]
	print(bot.blacklisted_users)
	print("Hey! I'm Terrabot!")
	print("I'm made by Pinkalicious21902")
	print("Who's ready to have a good time?")
	print(len(bot.commands))
	hel = ["Minecraft", "Bugging Pink", "Defending friends", "Tmodloader", "Juice WRLD", "Banning Bowling Pins", "scanning for rulebreakers", "I'm awesome!"]
	running = True
	while running == True:
		await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(hel)))
		await asyncio.sleep(30)
		await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(hel)))
	currentMutes = await bot.mutes.get_all()
	for mute in currentMutes:
		bot.muted_users[mute["_id"]] = mute


# channel = msg_dump_channel.get_channel(797235482110328884)
@bot.event
async def on_message(message):
	if message.guild is None and not message.author.bot:
		embed = discord.Embed(
			title = 'NEW MESSAGE!',
			description = '{}'.format(message.content),
			color = discord.Color.from_rgb(r=159, g=255, b=255)
			)
		embed.set_footer(text='Sent by {} | ID-{}'.format(message.author, message.author.id))
		for channel in bot.get_all_channels():
			if channel.name == "dms":
				await channel.send(embed=embed)

	
	# if message.guild is None and not message.author.bot:
	# 	# if the channel is public at all, make sure to sanitize this first
	# 	await channel.send(message.content)
	if message.author.id in bot.blacklisted_users:
		return
	#Respond with prefix if bot is pinged
	if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(
		f"<@!{bot.user.id}>"
	):
		data = await bot.config.find_by_id(message.guild.id)
		if not data or "prefix" not in data:
			prefix = config.command_prefixes
		else:
			prefix = data["prefix"]
		await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)
	await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
	channel = discord.utils.get(member.guild.text_channels, name="logs")
	if channel:
		embed = discord.Embed(description="Goodbye from each and every one of us...", color=random.choice(bot.color_list))
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_author(name=member.name, icon_url=member.avatar_url)
		embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
		embed.timestamp = datetime.datetime.utcnow()

		await channel.send(embed=embed)
def quote(query):
		# Strips all spaces, tabs, returns and replaces with + signs, then urllib quotes
		return query.replace("+","%2B").replace("\t","+").replace("\r","+").replace("\n","+").replace(" ","+")


@bot.command(hidden=True)
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.guild_only()
async def spamtwo(ctx, *, message):
	x=1
	await ctx.message.delete()
	while x<10:
		x += 1
		await ctx.send(message)
@bot.command(name='perms', aliases=['perms_for', 'permissions', 'userperms'])
async def check_permissions(ctx, member: discord.Member=None):
	"""A simple command which checks a members Guild Permissions.
	If member is not provided, the author will be checked."""
	if not member:
		member = ctx.author
	# Here we check if the value of each permission is True.
	perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
	# And to make it look nice, we wrap it in an Embed.
	embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
	embed.set_author(icon_url=member.avatar_url, name=str(member))
	# \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
	embed.add_field(name='\uFEFF', value=perms)
	await ctx.send(content=None, embed=embed)
@bot.command(name="wipe", aliases=["delete", "clean", "removespam"])
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number: int):
	"""Deletes a certain number of messages"""
	await ctx.trigger_typing()
	if number < 1 or number > 500:
		return await ctx.send("Please choose a number between 1 and 500")
	deleted = await ctx.channel.purge(limit=number)
	print('Deleted {} message(s)'.format(len(deleted)))
	logger.info('Deleted {} message(s)'.format(len(deleted)))
	await ctx.send("Deleted {} messages, my master.".format(len(deleted)), delete_after=5)
@bot.command(name="hostinfo")
async def hostinfo(ctx):
	"""
	A useful command that displays bot statistics.
	"""
	bot.version = 3.3
	pythonVersion = platform.python_version()
	dpyVersion = discord.__version__
	serverCount = len(bot.guilds)
	memberCount = len(set(bot.get_all_members()))

	embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

	embed.add_field(name='Bot Version:', value=bot.version)
	embed.add_field(name='Python Version:', value=pythonVersion)
	embed.add_field(name='Discord.Py Version', value=dpyVersion)
	embed.add_field(name='Total Guilds:', value=serverCount)
	embed.add_field(name='Total Users:', value=memberCount)
	embed.add_field(name='Bot Developers:', value="<@466778567905116170>")

	embed.set_footer(text=f"Made By | {bot.user.name}")
	embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

	await ctx.send(embed=embed)
@bot.command(name="reddit", description="Gets a random post from reddit", usage="<subreddit>")
@commands.cooldown(1, 15, commands.BucketType.user)
async def reddit(ctx, *, subreddit):
	import praw

	reddit = praw.Reddit(client_id = "9bSwwrbBPedZxQ", client_secret = "DD4byMeUmG_zv7lfCQ_ZzIDJniGnVg", username = "Terrariamaster2002", password = "@dA7xTbSZ7Hq_3_", user_agent = "pythonpraw")

	sub = reddit.subreddit(subreddit)
	all_subs = []

	top = sub.top(limit=50)

	for submission in top:
		all_subs.append(submission)

	random_sub = random.choice(all_subs)
	name = random_sub.title
	url = random_sub.url

	em = discord.Embed(title=name)
	em.set_image(url=url)

	await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 20,commands.BucketType.guild)
@bot_has_permissions(manage_messages=True)
@has_permissions(manage_messages=True)
async def purgeall(ctx):
	"""Deletes all messages in a channel"""
	await ctx.trigger_typing()
	await ctx.channel.purge(limit=None, check=lambda message: not message.pinned)
	await ctx.send("I have successfully cleared everything in this channel!")

@bot.command(help="Displays what a user is listening to on Spotify", usage="[user]")
async def spotify(ctx, user: discord.Member=None):
	user = user or ctx.author
	for activity in user.activities:
		if isinstance(activity, Spotify):
			em = discord.Embed(color=activity.color)
			em.title = f'{user.name} is listening to {activity.title}'
			em.set_thumbnail(url=activity.album_cover_url)
			em.description = f"**Song Name**: {activity.title}\n**Song Aetist**: {activity.artist}\n**Song Album**: {activity.album}\n**Song Lenght**: {pendulum.duration(seconds=activity.duration.total_seconds()).in_words(locale='en')}"
			await ctx.send(embed=em)
			break
	else:
		embed = discord.Embed(color=0xff0000)
		embed.title = f'{user.name} is not listening Spotify right now!'
		await ctx.send(embed=embed)

@bot.command(aliases=["makebig", "enlargen", "supersize"])
async def embiggen(ctx, *, text):
	"""Embiggens text. Yes that's a word, obviously"""
	await ctx.send("```fix\n" + figlet_format(text, font="big") + "```")

@bot.command()
async def terrariaquotes(ctx):
	"""Various messages from the game Terraria"""
	terrariaquote = open("terrariaquotes.txt").read().splitlines()
	terraria = random.choice(terrariaquote)
	await ctx.send(terraria)
@bot.command(aliases=["ud", "urbandict", "define"])
@commands.is_nsfw()
async def urban(ctx, *msg):
	"""Define stuff with Urban Dict"""
	print("hi")
	word = ' '.join(msg)
	api = "http://api.urbandictionary.com/v0/define"
	logger.info("Making request to " + api)
	
	# Send request to the Urban Dictionary API and grab info
	response = requests.get(api, params=[("term", f"```{word}```")]).json()
	embed = discord.Embed(description="No results found!", colour=0xFF0000)
	if len(response["list"]) == 0:
		return await ctx.send(embed=embed)
	# Add results to the embed
	print(word)
	if word == "Iroh":
		embed = discord.Embed(title="Word", description=word, color=embed.colour)
		embed.add_field(name="Top definition:", value="A screeching goblin that like minecraft too much")
		embed.add_field(name="Examples:", value="Oh that [{}]. Always playing MC.".format(word))
		return await ctx.send(embed=embed)
	
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
	embed2.add_field(name="Verification: ", value = str(guild.verification_level))
	embed2.add_field(name="Emojis", value=len(guild.emojis))
	embed.add_field(name="Icon:", value=guild.icon_url_as(static_format='webp', size=1024))
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
async def online(ctx):
	"""Get # of offline members"""
	# Set the filter to be a non-offline member, and the member not being a bot.
	def filterOnlyOnlineMembers(member):
		return member.status != discord.Status.offline
	membersInServer = ctx.guild.members
	onlineMembersInServer = list(filter(filterOnlyOnlineMembers, membersInServer))
	onlineMembersCount = len(onlineMembersInServer)
	await ctx.send("There are " + str(onlineMembersCount) + " Members online out of {}".format(len(ctx.guild.members)))

@bot.command(aliases=["nickchange", "changenick"])
@has_permissions(manage_nicknames=True)
@commands.cooldown(1, 20, commands.BucketType.user)
async def changenickname(ctx, member : discord.Member, *, nickname):
	"""Change a user's nickname"""
	if member == ctx.guild.owner:
		return await ctx.send("Cannot change the nick of the server owner!")
	await member.edit(nick=nickname)
	await ctx.send(f"Success! {member}'s Nickname changed to {nickname}")
@bot.command()
async def userinfo(ctx, member:discord.Member):
	"""Info about user"""
	embed = discord.Embed(title="User Info", color=0xff00ae)
	embed.add_field(name="Name: ", value=member.name)
	embed.add_field(name="web status", value=member.web_status)
	embed.add_field(name="On Mobile? ", value=member.is_on_mobile())
	embed.add_field(name="True Mobile Status ", value=member.mobile_status)
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
	embed = discord.Embed(title="Here you go!", description=message[::-1], color=0xff00ae)
	await ctx.send(embed=embed)

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
async def avatar(ctx, *,  user : discord.User):
	"""Gets a user's avatar"""
	userAvatarUrl = user.avatar_url
	await ctx.send(userAvatarUrl)

@bot.command(name="pi")
async def calculatepi(ctx, n:int):
	"""Calculate pi to a certain # of digits"""
	def roundpi(n):
		return round(math.pi, n)
	if n > 15:
		return await ctx.send("the maximum is 15 digits sadly.")
	await ctx.send(roundpi(n))
@bot.command(hidden=True, enabled=False)
@commands.is_nsfw()
async def rule34(ctx, *, tags:str):
	"""A wonderfun NSFW command"""
	await ctx.channel.trigger_typing()
	try:
		data = requests.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}".format(tags), headers=header).json()
	except json.JSONDecodeError as f:
		logger.error(f)
		await ctx.send(Language.get("nsfw.no_results_found", ctx).format(tags))
		return

	count = len(data)
	if count == 0:
		await ctx.send(Language.get("nsfw.no_results_found", ctx).format(tags))
		return
	image_count = 8
	if count < 8:
		image_count = count
	images = []
	for i in range(image_count):
		image = data[random.randint(0, count)]
		images.append("http://img.rule34.xxx/images/{}/{}".format(image["directory"], image["image"]))
	await ctx.send(("nsfw.results", ctx).format(image_count, count, tags, "\n".join(images)))
@bot.command(aliases=["cutedog", "randomdog"])
async def shibe(ctx):
	"""Sends a random shibe picture."""
	try:
		image = requests.get("http://shibe.online/api/shibes?count=1&urls=true").json()
		print(image[0])
		
		embed = discord.Embed()
		embed.set_image(url=image[0])
		await ctx.send(embed=embed)
		
	except aiohttp.ClientError as e:
		logger.error(e)
		await ctx.send(f"{ctx.tick(False)} Failed to grab a shibe. Try again later.")
@bot.command()
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
@commands.cooldown(1, 20,commands.BucketType.user)
async def setdelay(ctx, seconds: int):
	await ctx.channel.edit(slowmode_delay=seconds)
	await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
@bot.command(name="emojinames", description="Shows the names of recent custom emoji used. Useful for mobile users.")
@commands.guild_only()
@commands.has_permissions(read_message_history=True)
async def namesofemojis(ctx):
	from typing import Set
	import functools
	

	def reducer(emoji: Set[str], message: discord.Message):
		names = EMOJI_NAME_REGEX.findall(message.content)
		return emoji | set(names)

	messages = await ctx.history(limit=50).flatten()
	names: Set[str] = functools.reduce(reducer, messages, set())

	if not names:
		logger.error("No recently used custom emoji were found.")
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
	"""Have a meme, friend!"""
	embed = discord.Embed(title="Meme", description="Here comes a meme!!")
	async with aiohttp.ClientSession() as cs:
		async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
			res = await r.json()
			embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
			await ctx.send(embed=embed)

@bot.command()
async def suggest(ctx, *, suggestion:str):
	"""Sends a suggestion to the developers"""
	
	if isinstance(ctx.channel, discord.DMChannel):
		guild = "`No server! Sent via Private Message!`"
	else:
		guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
	msg = make_message_embed(ctx.author, 0xFF0000, suggestion, formatUser=True)
	owner = bot.get_user(466778567905116170)
	if owner:
		await owner.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
	for id in config.dev_ids:
		dev = bot.get_user(id)
		if dev:
			await dev.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)


@bot.command(aliases=["report", "notifydevs"])
async def notifydev(ctx, *, message:str):
	"""Sends a message to the developers"""
	if isinstance(ctx.channel, discord.DMChannel):
		guild = "`No server! Sent via Private Message!`"
	else:
		guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
	msg = make_message_embed(ctx.author, 0xFF0000, message, formatUser=True)
	owner = await bot.fetch_user(466778567905116170)
	await owner.send("You have received a new message! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
	await ctx.send(Language.get("bot.dev_notify", ctx).format(message))

if __name__ == '__main__':
	for file in os.listdir(cwd):
		if file.endswith(".py") and not file.startswith("_") and not file.startswith("bot.py") and not file.startswith("xphelp.py"):
			bot.load_extension(file[:-3])

	for file in os.listdir(cogdir):
		if file.endswith(".py") and not file.startswith("_") and not file.startswith("xphelp.py"):
			bot.load_extension(f"cogs.{file[:-3]}")
token = os.getenv('token')
bot.run(token)
