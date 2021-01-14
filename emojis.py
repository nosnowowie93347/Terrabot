import discord, random, asyncio, math
from random import choice, randint, randrange
from discord.ext import commands
emojilist = open("Emojis.txt", encoding='utf8').read().splitlines()


class Emoji(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
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

	# Get emotes from all servers
	@commands.command(aliases=["emoji", "emojis"], description="Displays all emotes avaiable on a server.")
	async def emotes(self, ctx):
		
		embed = discord.Embed(title="Emojis", description="Here are all the emojis available on the servers with Terrabot:", color=0x00ff00)  # setup embed
		
		for ej in ctx.message.guild.emojis:
			output = ej
			# Here we need 2 strings to add the backtick styling and avoid "too many arguments" errors
			output2 = ("```{}```".format(str(output)))
			# Add info to list (embed)
			embed.add_field(name=ej.name, value=output2, inline=False)
		await ctx.send(embed=embed)
	@commands.command()
	async def randomemoji(self, ctx):
		"""get a random emoji"""
		await ctx.send(random.choice(emojilist))


def setup(bot):
	bot.add_cog(Emoji(bot))