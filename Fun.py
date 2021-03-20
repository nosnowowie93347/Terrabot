import discord, random, base64, aiohttp, cat, hashlib, json, time, datetime, urllib, math, requests, asyncio, re, secrets, urllib, aiohttp, time, sys, importlib, os
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


punlist = open("Punlist.txt", encoding='utf8').read().splitlines()

def setup(bot):
	bot.add_cog(Fun(bot))


class Fun(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

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
	@commands.command(brief="Generates a random password string for you")
	async def password(self, ctx, nbytes: int = 18):
		if nbytes not in range(3, 1401):
			return await ctx.send("I only accept any numbers between 3-1400")
		if hasattr(ctx, 'guild') and ctx.guild is not None:
			await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
		await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")
	@commands.command()
	async def insult(self, ctx, member:discord.Member):
		"""Says something mean about you."""
		await ctx.send(member.mention + " " + random.choice(config.insults))

	@commands.command()
	async def coinflip(self, ctx):
		"""Flip a Frikin Coin"""
		await ctx.send(random.choice(coinsides))
	@commands.command(hidden=True, aliases=["changeavatar", "newavatar"])
	@commands.cooldown(1, 654, commands.BucketType.guild)
	@commands.is_owner()
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
	async def dm(self, ctx, member:discord.Member, *, message: str):
		""" DM the user of your choice """
		role = discord.utils.find(lambda r: r.name == 'nodm', ctx.guild.roles)
		user = member
		if not user:
			return await ctx.send(f"Could not find any UserID matching **{user_id}**")

		try:
			# if not role in user.roles:
			
			if role in user.roles:
				return await ctx.send("This user has the no dm role. This means they probably don't want DMs.")
			await ctx.send(f"✉️ Sent a DM to **{member.name}**")
			await user.send(message)
			await user.send(f"Message sent by: {ctx.author}")
		except discord.Forbidden:
			await ctx.send("This user might be having DMs blocked or it's a bot account...")

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
	@commands.is_nsfw()
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
	async def cat(self, ctx):
		"""Like the shibe command, but with cats."""
		cats = open("cats.txt").read().splitlines()
		cat2 = random.choice(cats)
		
		await ctx.send(cat2)
	@commands.command(description="What time is it?")
	async def clock(self, ctx):
		now = datetime.datetime.now()
		current_time = now.strftime("%H:%M:%S")
		await ctx.send(f"now = {current_time}")
