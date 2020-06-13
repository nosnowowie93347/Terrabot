import asyncio, random
import discord
from   Cogs import Nullify
from   Cogs import DisplayName
from   Cogs import Message
from   discord.ext import commands
from discord.ext.commands import Bot
import json
import os
import mtranslate

def setup(bot):
	# Add the bot and deps
	settings = bot.get_cog("Settings")
	bot.add_cog(Translate(bot, settings))

# Requires the mtranslate module be installed

class Translate(commands.Cog):
			
	def __init__(self, bot, settings, language_file = "Languages.json"):
		self.bot = bot
		self.settings = settings
		global Utils, DisplayName
		Utils = self.bot.get_cog("Utils")
		DisplayName = self.bot.get_cog("DisplayName")

		if os.path.exists(language_file):
			f = open(language_file,'r')
			filedata = f.read()
			f.close()
			self.languages = json.loads(filedata)
		else:
			self.languages = []
			print("No {}!".format(language_file))

	@commands.command(pass_context=True)
	async def langlist(self, ctx):
		"""Lists available languages."""
		if not len(self.languages):
			await ctx.send("I can't seem to find any languages :(")
			return
		description = ""
		for lang in self.languages:
			description += "**{}** - {}\n".format(lang["name"], lang["code"])
		embed = discord.Embed(title="Langs", description=description, footer="Note - some languages may not be supported.")
		await ctx.send(embed=embed)
	@commands.command(pass_context=True)
	async def tr(self, ctx, *, translate = None):
		"""Translate some stuff!"""
		usage = "Usage: `{}tr [words] [from code (optional)] [to code]`".format(ctx.prefix)
		if translate == None:
			await ctx.send(usage)
			return

		word_list = translate.split(" ")

		if len(word_list) < 2:
			await ctx.send(usage)
			return

		lang = word_list[len(word_list)-1]
		from_lang = word_list[len(word_list)-2] if len(word_list) >= 3 else "auto"

		# Get the from language
		from_lang_back = [ x for x in self.languages if x["code"].lower() == from_lang.lower() ]
		from_lang_code = from_lang_back[0]["code"] if len(from_lang_back) else "auto"
		from_lang_name = from_lang_back[0]["name"] if len(from_lang_back) else "Auto"
		# Get the to language
		lang_back = [ x for x in self.languages if x["code"].lower() == lang.lower() ]
		lang_code = lang_back[0]["code"] if len(lang_back) else None
		lang_name = lang_back[0]["name"] if len(lang_back) else None

		# Translate all but our language codes
		if len(word_list) > 2 and word_list[len(word_list)-2].lower() == from_lang_code.lower():
			trans = " ".join(word_list[:-2])
		else:
			trans = " ".join(word_list[:-1])
		
		if not lang_code:
			embed = discord.Embed(title="Something went wrong...", description="I couldn't find that language!", color=0xf1c40f)
			await ctx.send(embed=embed)
			return

		result = mtranslate.translate(trans, lang_code, from_lang_code)
		
		if not result:
			embed = discord.Embed(title="Something went wrong...", description="I wasn't able to translate that!", color=0xf1c40f)
			await ctx.send(embed=embed)
			return
		
		if result == trans:
				# We got back what we put in...
				embed = discord.Embed(title="Something went wrong...", description="The text returned from Google was the same as the text put in.  Either the translation failed - or you were translating from/to the same language (en -> en)")
				await ctx.send(embed=embed)
				return

		embed = discord.Embed(title="your translation is:", description=result, footer="{} --> {} - Powered by Google Translate".format(from_lang_name, lang_name))
		await ctx.send(embed=embed)
	@commands.command(pass_context=True)
	async def drbeer(self, ctx):
		"""Put yourself in your place."""
		
		beerList = ["Hey, yall. Quit ya horsin' around now. Can't you see I'm busy tryin'a shoot'n all them summersquash?",
					"Now I don't know how to use all them 5-dollah words y'all sprayin' around, but sure seems to me like y'all need to mind your peas and queues.",
					"As long as I can keep practicin' and protectin' all my favorite amendments, like the second and thirty-first, I am all dandy.",
					"Woah there, buckaroo! That's a mighty harsh language from someone communicating through a tube in the ocean over the internets.",
					"Now, I don't mind y'all people, but you keep botherin' me when I'm tryin'a enjoy my cold Bud in this beautiful, patriotic sunset. Haven't yall folks got better things to do then keep arguing and snicker in' around when y'all should be worried about the government and the N, S & A listenin'?",
					"Well, my daddy always said a man is only as good as his words and the thrust and torque of his good ole John Deere."]
		# Remove original message
		await ctx.message.delete()
		# Say new message
		await ctx.send(random.choice(beerList))