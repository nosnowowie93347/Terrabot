import asyncio
import contextlib
import datetime
import json
import logging
import pathlib
import random
import re

import aiohttp
import dateparser
import discord
from discord.ext import commands
from discord.ext.commands import Converter, BadArgument
from utilities import inline


ENDPOINT = "https://byabbe.se/on-this-day/{}/events.json"

DEFAULT_DESCRIPTION = """
Please send a valid year from the list of years below. Only years above 0 are included.
"""

MONTH_MAPPING = {
    "1": "january",
    "2": "february",
    "3": "march",
    "4": "april",
    "5": "may",
    "6": "june",
    "7": "july",
    "8": "august",
    "9": "september",
    "10": "october",
    "11": "november",
    "12": "december",
}


def check(ctx: commands.Context):
    return lambda x: x.author == ctx.author and x.channel == ctx.channel


def highlight_numerical_data(string):
    return re.sub(r"(([\d{1}],?)+)", r"**\1**", string)


def retrieve_above_0(year):
    return year.strip().isdigit()


def columns(years):
    m = f"{chr(12644)}\n"  # padding
    f = lambda s: inline(s.zfill(4))
    for x in range(6, len(years), 6):
        m += "\n" + (" " * 5).join(map(f, years[x - 6 : x]))
    return m


def date_suffix(number) -> str:
    number = int(number)
    suffixes = {0: "th", 1: "st", 2: "nd", 3: "rd"}
    for i in range(4, 10):
        suffixes[i] = "th"
    return str(number) + suffixes[int(str(number)[-1])]


def now() -> datetime.datetime:
    return datetime.datetime.now()


class DateConverter(Converter):
    """Date converter which uses dateparser.parse()."""

    async def convert(self, ctx: commands.Context, arg: str) -> datetime.datetime:
        parsed = dateparser.parse(arg)
        if parsed is None:
            raise BadArgument("Unrecognized date/time.")
        if parsed.strftime("%Y") != str(now().strftime("%Y")):
            raise BadArgument("Please do not specify a year.")
        return parsed


class OnThisDay(commands.Cog):
    """Find out what happened today, in multiple different years in history."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def run_otd(
        self,
        ctx: commands.Context,
        month_number,
        date_number,
        year,
        _random: bool = False,
    ):
        """Oh my, is this scruffy code... but it WORKS!"""
        try:
            async with self.session.get(
                ENDPOINT.format(f"{month_number}/{date_number}")
            ) as session:
                if session.status != 200:
                    return await ctx.send(
                        "An error occured whilst retrieving information for this day."
                    )
                content = await session.json()
        except aiohttp.ClientError as e:
            log.exception(e)
            return await ctx.send(
                "An error occured whilst retrieving information for this day."
            )
        else:
            wikipedia_for_the_day = content["wikipedia"]
            events = filter(lambda x: retrieve_above_0(x["year"]), content["events"])
            data = {
                e["year"]: {"content": e["description"], "wikipedia": e["wikipedia"]}
                for e in events
            }
            if _random:
                result = random.choice(list(data.keys()))
            else:
                message = f"**Events for this day ({MONTH_MAPPING[month_number].capitalize()} the {date_suffix(date_number)})**\n"
                await ctx.send(
                    message + DEFAULT_DESCRIPTION + columns(list(data.keys()))
                )
                try:
                    message = await self.bot.wait_for(
                        "message", check=check(ctx), timeout=50
                    )
                except asyncio.TimeoutError:
                    return await ctx.send("You took too long to respond.")
                container = tuple(data.keys())
                if (result := message.content.lstrip("0")) not in container:
                    return await ctx.send(
                        f"{inline(result)} was not a valid year for this day."
                    )
            event = data[result]
            years_ago = int(year) - int("".join(filter(str.isdigit, result)))
            embed = discord.Embed(
                title=f"On this day, {years_ago} years ago...",
                description=highlight_numerical_data(event["content"]),
            )
            embed.set_footer(text="Year: " + result)
            embed.add_field(
                name="Specific Wikipedia Links",
                value="\n".join(
                    f"- [{w['title']}]({w['wikipedia']})" for w in event["wikipedia"]
                ),
            )
            _d = {
                f"Other important events that occured in the year {result}...": "https://en.wikipedia.org/wiki/"
                + result,
                f"Other important events that occured on {MONTH_MAPPING[month_number]} the {date_suffix(date_number)} in history...": wikipedia_for_the_day,
            }
            embed.add_field(
                name="Other links",
                value="\n".join(f"- [[{k}]]({v})" for k, v in _d.items()),
                inline=False,
            )
            await ctx.send(embed=embed)

    @commands.has_permissions(embed_links=True)
    @commands.group(invoke_without_command=True, aliases=["otd"])
    async def onthisday(self, ctx, *, day: DateConverter = None):
        """Find out what happened on this day, in various different years!
        If you want to specify your own date, you can do so by using
        `[p]onthisday [day]`.
        You can also receive a random year by using `[p]onthisday random [day]`.
        """
        await ctx.trigger_typing()
        if day is None:
            day = now()
        month_number = day.strftime(r"%m").lstrip("0")
        date_number = day.strftime(r"%d").lstrip("0")
        year = day.strftime(r"%Y")
        await self.run_otd(ctx, month_number, date_number, year, False)

    @onthisday.command()
    async def random(self, ctx, *, day: DateConverter = None):
        """Find out what happened on this day, in a random year.
        If you want to specify your own date, you can do so by using
        `[p]onthisday random [day]`.
        """
        await ctx.trigger_typing()
        if day is None:
            day = now()
        month_number = day.strftime(r"%m").lstrip("0")
        date_number = day.strftime(r"%d").lstrip("0")
        year = day.strftime(r"%Y")
        await self.run_otd(ctx, month_number, date_number, year, True)


def setup(bot):
    bot.add_cog(OnThisDay(bot))
