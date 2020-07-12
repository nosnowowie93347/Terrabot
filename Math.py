import math, discord, aiohttp, os, requests, sys
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
class Math(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	async def calculator(self, ctx):
		pass
		
	@calculator.command(pass_context=True)
	async def add(self, ctx, a: int, b:int):
		await ctx.send(a+b)
		
	@calculator.command(pass_context=True)
	async def subtract(self, ctx, a: int, b:int):
		await ctx.send(a-b)
		
	@calculator.command(pass_context=True)
	async def multiply(self, ctx, a: int, b:int):
		await ctx.send(a*b)
		
	@calculator.command(pass_context=True)
	async def divide(self, ctx, a: int, b:int):
		try:
			await ctx.send(a/b)
		except ZeroDivisionError as e:
			return await ctx.send(e)
	@calculator.command(pass_context=True)
	async def sqrt(self, ctx, a: int):
		try:
			string1 = "The square root of "
			await ctx.send(f"{string1} {a} is {math.sqrt(a)}")
		except ValueError as e:
			await ctx.send(e, "Only positive #s can be sqrted.")
	@calculator.command()
	async def sin(self, ctx, a: int):
		await ctx.send(f"The sine of {a} is {math.sin(a)}")
	@calculator.command()
	async def cos(self, ctx, a:int):
		await ctx.send(f"The cosine of {a} is {math.cos(a)}")
def setup(bot):
	bot.add_cog(Math(bot))