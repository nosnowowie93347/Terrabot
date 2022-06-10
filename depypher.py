import discord, functools
from typing import Callable, Final, List, Literal, Optional

from pycipher import pycipher
from discord.ext import commands

_caesar: Final[pycipher.Caesar] = pycipher.Caesar(key=4)
_atbash: Final[pycipher.Atbash] = pycipher.Atbash()
_vigenere = pycipher.Vigenere
_porta = pycipher.Porta


def convert_case(original: str, new: str) -> str:
    ret = ""
    for (
        index,
        letter,
    ) in enumerate(original):
        if not letter.isalpha():
            ret += letter
            new = f"{new[:index]}{letter}{new[index + 1:]}"
            continue
        if letter.isupper():
            ret += new[index].upper()
        else:
            ret += new[index].lower()
    return ret


class Depypher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def caesar(self, ctx, *, message: str):
        await self._process_message(
            ctx, _caesar.encipher(string=message, keep_punct=True), message
        )

    @commands.command()
    async def decaesar(self, ctx, *, cipher: str):
        await self._process_message(
            ctx, _caesar.decipher(string=cipher, keep_punct=True), cipher
        )

    @commands.command()
    async def vigenere(self, ctx, keyword: str, *, message: str):
        await self._process_message(
            ctx, _vigenere(key=keyword).encipher(message), message
        )

    @commands.command()
    async def devigenere(self, ctx, keyword: str, *, cipher: str):
        await self._process_message(
            ctx, _vigenere(key=keyword).decipher(cipher), cipher
        )

    @commands.command()
    async def porta(self, ctx, keyword: str, *, message: str):
        await self._process_message(ctx, _porta(key=keyword).encipher(message), message)

    @commands.command()
    async def deporta(self, ctx, keyword: str, *, cipher: str):
        await self._process_message(ctx, _porta(key=keyword).decipher(cipher), cipher)

    @staticmethod
    async def _process_message(
        ctx: commands.Context, msg: str, original: str
    ) -> discord.Message:
        async with ctx.typing():
            case = functools.partial(convert_case, original, msg)
            processed = await ctx.bot.loop.run_in_executor(None, case)
        return await ctx.send(processed)


def setup(bot):
    bot.add_cog(Depypher(bot))
