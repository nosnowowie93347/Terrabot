import discord, random, requests, io, json, aiohttp, re
from bs4 import BeautifulSoup
from discord import ext
from discord.ext import commands
from random import choice, randint
from discord.ext.commands import Bot
import platform, asyncio


class Cog3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(description="Make fancy text!")
    async def fancify(self, ctx, *, text):
        def strip_non_ascii(string):
            """Returns the string without non ASCII characters."""
            stripped = (c for c in string if 0 < ord(c) < 127)
            return "".join(stripped)

        text = strip_non_ascii(text)
        if len(text.strip()) < 1:
            return await self.ctx.send(":x: ASCII characters only please!")
        output = ""
        for letter in text:
            if 65 <= ord(letter) <= 90:
                output += chr(ord(letter) + 119951)
            elif 97 <= ord(letter) <= 122:
                output += chr(ord(letter) + 119919)
            elif letter == " ":
                output += " "
        await ctx.send(output)

    @commands.command()
    @commands.guild_only()
    async def echo(self, ctx, *, message):
        """Makes the bot talk."""
        say = message
        await ctx.message.delete()
        return await ctx.send(say)

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """Lists the roles for the current guild"""
        roles = ctx.guild.roles
        embed = discord.Embed(title="**The roles on this server are: **")
        for role in roles:
            embed.add_field(name=role.name, value=role.name)
        await ctx.send(embed=embed)

    @commands.command(description="Really awful jokes. Courtesy of icanhazdadjoke.com")
    async def dadjoke(self, ctx):
        import requests

        channel = ctx.message.channel
        author = ctx.message.author
        server = ctx.message.guild
        joke = requests.get(
            "https://icanhazdadjoke.com", headers={"Accept": "text/plain"}
        ).text
        await ctx.send(joke)

    @commands.command(aliases=["diceroll", "rolladice"])
    async def roll(self, ctx):
        """Roll a Frikin Die"""
        await ctx.send("You rolled a " + str(randint(1, 20)))

    @commands.bot_has_permissions(attach_files=True)
    @commands.command()
    async def xkcd(self, ctx):
        """
        XKCD
        https://xkcd.com/
        """

        url = "https://c.xkcd.com/random/comic/"
        phrase = r"Image URL \(for hotlinking\/embedding\)\:.*"

        async with ctx.typing():
            async with self.session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")

            img_url_nav_string = soup.find(text=re.compile(phrase))
            img_url = img_url_nav_string.find_next_sibling("a").text

            async with self.session.get(img_url) as response:
                img = io.BytesIO(await response.read())

            await ctx.send(file=discord.File(img, "xkcd.png"))


def setup(bot):
    bot.add_cog(Cog3(bot))
