import math, discord, aiohttp, os, requests, sys
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions
class Math(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(description="Adds 2 numbers", usage="<number1> <number2>")
	async def add(self, ctx, a: int, b:int):
		await ctx.send(a+b)
		
	@commands.command(description="Subtracts 2 numbers", usage="<number1> <number2>")
	async def subtract(self, ctx, a: int, b:int):
		await ctx.send(a-b)
		
	@commands.command(description="Multiplies 2 numbers", usage="<number1> <number2>")
	async def multiply(self, ctx, a: int, b:int):
		await ctx.send(a*b)
		
	@commands.command(description="Divides 2 numbers", usage="<number1> <number2>")
	async def divide(self, ctx, a: int, b:int):
		try:
			await ctx.send(a/b)
		except ZeroDivisionError as e:
			return await ctx.send(e)
	@commands.command(description="Square root a number", usage="<number>")
	async def sqrt(self, ctx, a: int):
		try:
			await ctx.send(f"The square root of {a} is {math.sqrt(a)}")
		except ValueError as e:
			await ctx.send("Only positive #s can be sqrted.")
	@commands.command(description="Find the sine of a number", usage="<number>")
	async def sin(self, ctx, a: int):
		await ctx.send(f"The sine of {a} is {math.sin(a)}")
	@commands.command(description="Find the cosine of a number", usage="<number>")
	async def cos(self, ctx, a:int):
		await ctx.send(f"The cosine of {a} is {math.cos(a)}")
def setup(bot):
	bot.add_cog(Math(bot))