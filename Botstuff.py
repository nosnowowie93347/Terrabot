import discord, platform, requests, json, random, fnmatch, time, asyncio, os, datetime, tabulate
from discord import ext, Colour
from time import monotonic
from discord.ext.commands.converter import ColourConverter, PartialEmojiConverter
from discord.ext.commands.errors import BadColourArgument, PartialEmojiConversionFailure
from discord.ext import commands
from utils.language import Language
from utils.mysql import *
from utils.channel_logger import Channel_Logger
from utils.tools import *
from utils import checks, default
from discord.ext.commands import (
    Bot,
    has_permissions,
    bot_has_permissions,
    MissingPermissions,
)

bot_status = discord.Status.online


def box(text: str, lang: str = "") -> str:
    """Get the given text in a code block.
    Parameters
    ----------
    text : str
            The text to be marked up.
    lang : `str`, optional
            The syntax highlighting language for the codeblock.
    Returns
    -------
    str
            The marked up text.
    """
    return f"```{lang}\n{text}\n```"


class Botstuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startTime = int(time.time())

    @commands.command(
        description="Outputs the total count of lines of code in the currently installed repo."
    )
    @commands.guild_only()
    async def cloc(self, ctx):

        # Script pulled and edited from https://github.com/kyco/python-count-lines-of-code/blob/python3/cloc.py

        path = os.getcwd()

        # Set up some lists
        extensions = []
        code_count = []
        include = ["py", "bat", "sh", "command"]

        # Get the extensions - include our include list
        extensions = self.get_extensions(path, include)

        for run in extensions:
            extension = "*." + run
            temp = 0
            for root, dir, files in os.walk(path):
                for items in fnmatch.filter(files, extension):
                    value = root + "/" + items
                    temp += sum(+1 for line in open(value, "rb"))
            code_count.append(temp)
            pass

        # Set up our output
        msg = "Some poor soul took the time to sloppily write the following to bring me life:\n```\n"
        padTo = 0
        for idx, val in enumerate(code_count):
            # Find out which has the longest
            tempLen = len(str("{:,}".format(code_count[idx])))
            if tempLen > padTo:
                padTo = tempLen
        for idx, val in enumerate(code_count):
            lineWord = "lines"
            if code_count[idx] == 1:
                lineWord = "line"
            # Setup a right-justified string padded with spaces
            numString = str("{:,}".format(code_count[idx])).rjust(padTo, " ")
            msg += numString + " " + lineWord + " of " + extensions[idx] + "\n"
            # msg += extensions[idx] + ": " + str(code_count[idx]) + ' ' + lineWord + '\n'
            # print(extensions[idx] + ": " + str(code_count[idx]))
            pass
        msg += "```"
        await ctx.send(msg)

    def get_extensions(self, path, excl):
        extensions = []
        for root, dir, files in os.walk(path):
            for items in fnmatch.filter(files, "*"):
                temp_extensions = items.rfind(".")
                ext = items[temp_extensions + 1 :]
                if ext not in extensions:
                    if ext in excl:
                        extensions.append(ext)
                        pass
        return extensions

    @commands.command(description=" Check when a user joined the current server ")
    @commands.guild_only()
    async def joinedat(self, ctx, *, user: discord.Member = None):

        user = user or ctx.author

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = (
            f"**{user}** joined **{ctx.guild.name}**\n{default.date(user.joined_at)}"
        )
        await ctx.send(embed=embed)

    @commands.command(description="About the Bot")
    @commands.guild_only()
    async def about(self, ctx):
        embed = discord.Embed(
            color=0x676767, description=str(len(self.bot.commands)) + " commands"
        )
        embed.add_field(name="Website", value="http://nosnowowie93347.github.io/")
        embed.set_author(
            name="Terrabot",
            icon_url="https://cdn.discordapp.com/avatars/657372691749273612/67d2caa88aad928296c23b2aa964384d.webp?size=1024",
        )
        embed.set_footer(text="Terrabot | Created by Pinkalicious21902")
        embed.add_field(
            name="What is Terrabot?",
            value="Terrabot is a general purpose bot built on the discord.py library. The bot began as a fun project and will continue to have updates pushed out as I learn more.",
        )
        embed.add_field(
            name="Need help on how to use it?",
            value="You can check the help command by doing \n\n``^help`` \n\n Updates will constantly be pushed out with more features and new commands.",
        )
        embed.add_field(name="Thanks to Sukuya for inspiration.", value=":smile:")
        await ctx.send(embed=embed)

    @commands.command(
        name="platform", description="Tells the platform the bot's running on"
    )
    @commands.guild_only()
    async def platforms(self, ctx):
        await ctx.send(
            "The bot is currently running on: ```" + str(platform.platform()) + "```"
        )

    @commands.command(description="Lists the servers Terrabot is in")
    @commands.guild_only()
    async def serverlist(self, ctx):
        x = ", ".join([str(server) for server in self.bot.guilds])
        y = len(self.bot.guilds)
        print("Server list: " + x)
        if y > 40:
            thing = (
                "Currently active on " + str(y) + " servers:",
                "fuck" + "```json\nCan't display more than 40 servers!```",
            )
            await ctx.send(thing)
        elif y < 40:
            thing2 = (
                "Currently active on " + str(y) + " servers:" + "```json\n" + x + "```"
            )
            await ctx.send(thing2)

    @commands.command(
        aliases=["pinf", "pig", "png", "pign", "pjgn", "ipng", "pgn", "pnig"]
    )
    @commands.guild_only()
    async def ping(self, ctx: commands.Context):
        """
        A rich embed ping command with timings.
        This will show the time to send a message, and the WS latency to Discord.
        If I can't send embeds or they are disabled here, I will send a normal message instead.
        The embed has more detail and is preferred.
        """
        try:
            ws_latency = round(self.bot.latency * 1000)
        except OverflowError:  # ping float is infinity, ie last ping to discord failed
            await ctx.send(
                "I'm alive and working normally, but I've had connection issues in the last few "
                "seconds so precise ping times are unavailable. Try again in a minute."
            )
            return

        title = "\N{TABLE TENNIS PADDLE AND BALL}  Pong!"

        if ctx.guild:

            use_embed = ctx.channel.permissions_for(ctx.me).embed_links  # type:ignore
        embed: discord.Embed | None = None

        if use_embed:
            embed = discord.Embed(title=title)
            embed.add_field(name="Discord WS", value=box(f"{ws_latency} ms", "py"))

            start = monotonic()
            message: discord.Message = await ctx.send(embed=embed)
        else:
            msg = f"**{title}**\nDiscord WS: {ws_latency} ms"
            start = monotonic()
            message = await ctx.send(msg)
        end = monotonic()

        # im sure there's better way to do these long ifs, haven't looked properly yet

        m_latency = round((end - start) * 1000)

        ws_latency_text, m_latency_text = self._get_latency_text(
            ws_latency, m_latency, use_embed
        )

        if use_embed and embed is not None:
            colour = Colour.random()
            extra = box(f"{ws_latency} ms", "py")
            embed.set_field_at(0, name="Discord WS", value=f"{ws_latency_text}{extra}")
            extra = box(f"{m_latency} ms", "py")
            embed.add_field(name="Message Send", value=f"{m_latency_text}{extra}")
            embed.colour = colour
            await message.edit(embed=embed)
        else:
            data = [
                ["Discord WS", "Message Send"],
                [ws_latency_text, m_latency_text],
                [f"{ws_latency} ms", f"{m_latency} ms"],
            ]
            table = box(
                tabulate.tabulate(data, tablefmt="plain"), "py"
            )  # cspell: disable-line
            msg = f"**{title}**{table}"
            await message.edit(content=msg)

    # im sure there's better way to do these two methods but i cba to find one

    def _get_latency_text(
        self, ws_latency: int, m_latency: int, emojis: bool
    ) -> tuple[str, str]:
        if ws_latency < 50:
            ws_latency_text = ":green_square: Excellent" if emojis else "Excellent"
        elif ws_latency < 150:
            ws_latency_text = ":green_square: Good" if emojis else "Good"
        elif ws_latency < 250:
            ws_latency_text = ":orange_square: Alright" if emojis else "Alright"
        elif ws_latency < 500:
            ws_latency_text = ":red_square: Bad" if emojis else "Bad"
        else:
            ws_latency_text = ":red_square: Very Bad" if emojis else "Very Bad"

        if m_latency < 75:
            m_latency_text = ":green_square: Excellent" if emojis else "Excellent"
        elif m_latency < 225:
            m_latency_text = ":green_square: Good" if emojis else "Good"
        elif m_latency < 350:
            m_latency_text = ":orange_square: Alright" if emojis else "Alright"
        elif m_latency < 600:
            m_latency_text = ":red_square: Bad" if emojis else "Bad"
        else:
            m_latency_text = ":red_square: Very Bad" if emojis else "Very Bad"

        return ws_latency_text, m_latency_text

    @commands.command(aliases=["logout"], description="Shuts down the bot.")
    @commands.is_owner()
    async def shutdown(self, ctx):

        await ctx.send("logging out...")
        await self.bot.logout()

    @commands.command(description="Unpins the message with the specified ID")
    @commands.guild_only()
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def unpin(self, ctx, id: int):
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        if message is None:
            await ctx.send(
                Language.get("moderation.no_pinned_message_found", ctx).format(id)
            )
            return
        try:
            await message.unpin()
            await ctx.send(Language.get("moderation.unpin_success", ctx))
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))

    @commands.command(description="Sends the bot's OAuth2 link")
    @commands.guild_only()
    async def inviteme(self, ctx):
        await ctx.send(
            Language.get("bot.joinserver", ctx).format(
                "https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927"
            )
        )
        await ctx.author.send(
            Language.get("bot.joinserver", ctx).format(
                "https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927"
            )
        )


def setup(bot):
    bot.add_cog(Botstuff(bot))
