import discord, io, textwrap, contextlib, aiohttp, sys, subprocess, logging, typing, traceback, json, os, requests, datetime, time, operator, math, asyncio
from pathlib import Path
from discord.ext import commands
from utils.logger import log
import utils.json_loader
from traceback import format_exception
from utils.util import Pag, clean_code
import discord.utils
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions, bot_has_permissions
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logfile = 'discord.log'
handler = logging.FileHandler(filename=logfile, encoding='utf-8', mode='w')
blacklisted_users = []
cwd = Path(__file__).parents[0]
cwd = str(cwd)

def setup(bot):
	bot.add_cog(Ownercommands(bot))

class Ownercommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=["attachfile"])
	@commands.is_owner()
	async def uploadfile(self, ctx, *, path:str):
		"""Uploads any file on the system. What is this hackery?"""
		await ctx.channel.trigger_typing()
		try:
			await ctx.send(file=discord.File(path))
		except FileNotFoundError:
			print(path)
			await ctx.send("That file does not exist!")
	@commands.command(hidden=False, aliases=["reboot"])
	@commands.is_owner()
	async def restart(self, ctx):
		"""Restarts the bot"""
		await ctx.send("Restarting...")
		log.warning("{} has restarted the bot!".format(ctx.author))
		try:
		  await aiosession.close()
		except:
		   pass
		await self.bot.close()
		subprocess.call([sys.executable, "bot.py"])
	@commands.command(
		name="blacklist", description="Blacklist a user from the bot", usage="<user>"
	)
	@commands.is_owner()
	async def blacklist(self, ctx, user: discord.User):
		if user.id in self.bot.owner_ids:
			await ctx.send("Cant blacklist an owner")
			return
		if user.id in self.bot.blacklisted_users:
			return await ctx.send("Cannot blacklist someone twice! :person_facepalming:")
		if ctx.message.author.id == user.id:
			await ctx.send("Hey, you cannot blacklist yourself!")
			return

		self.bot.blacklisted_users.append(user.id)
		data = utils.json_loader.read_json("blacklist")
		data["blacklistedUsers"].append(user.id)
		utils.json_loader.write_json(data, "blacklist")
		await ctx.send(f"Hey, I have blacklisted {user.name} for you.")
		print(self.bot.blacklisted_users)

	@commands.command(
		name="unblacklist",
		description="Unblacklist a user from the bot",
		usage="<user>",
	)
	@commands.is_owner()
	async def unblacklist(self, ctx, user: discord.Member):
		"""
		Unblacklist someone from the bot
		"""
		self.bot.blacklisted_users.remove(user.id)
		data = utils.json_loader.read_json("blacklist")
		data["blacklistedUsers"].remove(user.id)
		utils.json_loader.write_json(data, "blacklist")
		await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")
	@commands.command()
	async def get_blacklists(self, ctx):
		data = utils.json_loader.read_json("blacklist")
		await ctx.send(data)
	@commands.command(name="eval", aliases=["exec"], description="Evaluates Python code")
	@commands.is_owner()
	async def _eval(self, ctx, *, code):
		code = clean_code(code)

		local_variables = {
			"discord": discord,
			"commands": commands,
			"bot": self.bot,
			"ctx": ctx,
			"channel": ctx.channel,
			"author": ctx.author,
			"guild": ctx.guild,
			"message": ctx.message
		}

		stdout = io.StringIO()

		try:
			with contextlib.redirect_stdout(stdout):
				exec(
					f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
				)

				obj = await local_variables["func"]()
				result = f"{stdout.getvalue()}\n-- {obj}\n"
		except Exception as e:
			result = "".join(format_exception(e, e, e.__traceback__))

		pager = Pag(
			timeout=100,
			entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
			length=1,
			prefix="```py\n",
			suffix="```"
		)

		await pager.start(ctx)
	@commands.command(name="toggle", description="Enable or disable a command")
	@commands.is_owner()
	async def toggle(self, ctx, *, command):
		command =  self.bot.get_command(command)

		if command is None:
			await ctx.send("I can't find a command with that name!")

		elif ctx.command == command:
			await ctx.send("This command cannot be disabled")

		else:
			command.enabled = not command.enabled
			variable = "enabled" if command.enabled else "disabled"
			await ctx.send(f"I have {variable} {command.qualified_name} for you.")
