import discord, random
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot
import platform, asyncio
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def EightBall(self, ctx, *, question = None):
        if question == None:
            await ctx.send("ask a question.")
        responses = [
        "It is certain",
        "Without a doubt",
        "You may rely on it",
        "Yes definitely",
        "It is decidedly so",
        "As I see it, yes",
        "Most likely",
        "Yes",
        "Outlook good",
        "Signs point to yes",
        "Reply hazy try again",
        "Better not tell you now",
        "Ask again later",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "Outlook not so good",
        "My sources say no",
        "Very doubtful",
        "My reply is no"
    ]

        
        answer = random.choice(responses)
        await ctx.send(f"The Magic 8 Ball says: {answer}")
def setup(bot):
    bot.add_cog(Fun(bot))