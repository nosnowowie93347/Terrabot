from random import randrange
import discord, os
from discord.ext import commands
from discord.ext.commands import Bot



class Skyrim(commands.Cog):
    """
    Says a random line from Skyrim.
    """
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def guard(self, ctx):
        """
        Says a random guard line from Skyrim.
        """
        cwd = os.getcwd()
        filepath = cwd + "/data/lines.txt"
        with open(filepath) as file:
            line = next(file)
            for num, readline in enumerate(file):
                if randrange(num + 2):
                    continue
                line = readline
        await ctx.send(line)

    @commands.command()
    async def nazeem(self, ctx):
        """
        Do you get to the Cloud District very often?
        Oh, what am I saying, of course you don't.
        """
        await ctx.send(
            "Do you get to the Cloud District very often? Oh, what am I saying, of course you don't."
        )
def setup(bot):
    bot.add_cog(Skyrim(bot))