import contextlib
import io
import json
import pathlib

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import python_minifier as minifier


class Minifier(commands.Cog):
    """Minify your code!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(attach_files=True)
    @commands.command(usage="<file>")
    async def minify(self, ctx):
        """Minify a python file.
        You need to attach a file to this command, and it's extension needs to be `.py`.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        file = ctx.message.attachments[0]
        file_name = file.filename.lower()
        if not file_name.endswith((".py", ".python")):
            return await ctx.reply("Must be a python file.")
        try:
            file = await file.read()
        except UnicodeDecodeError:
            return await ctx.reply(
                "Something went wrong when trying to decode this file."
            )
        converted = io.BytesIO(minifier.minify(file).encode(encoding="utf-8"))
        return await ctx.send(
            content="Please see the attached file below, with your minified code.",
            file=discord.File(converted, filename=file_name),
        )


def setup(bot):
    bot.add_cog(Minifier(bot))
