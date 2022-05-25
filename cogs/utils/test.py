import asyncio, contextlib, functools
from types import MappingProxyType
from typing import Callable, Iterable, List, Mapping, Optional, TypeVar, Union, SupportsInt, Sequence, Iterator

import discord

from discord.ext import commands
from .test2 import ReactionPredicate

_T = TypeVar("_T")
_PageList = TypeVar("_PageList", List[str], List[discord.Embed])
_ReactableEmoji = Union[str, discord.Emoji]
_ControlCallable = Callable[[commands.Context, _PageList, discord.Message, int, float, str], _T]

def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
    """Get text with all mass mentions or markdown escaped.
    Parameters
    ----------
    text : str
        The text to be escaped.
    mass_mentions : `bool`, optional
        Set to :code:`True` to escape mass mentions in the text.
    formatting : `bool`, optional
        Set to :code:`True` to escape any markdown formatting in the text.
    Returns
    -------
    str
        The escaped text.
    """
    if mass_mentions:
        text = text.replace("@everyone", "@\u200beveryone")
        text = text.replace("@here", "@\u200bhere")
    if formatting:
        text = discord.utils.escape_markdown(text)
    return text
async def menu(
    ctx: commands.Context,
    pages: _PageList,
    controls: Optional[Mapping[str, _ControlCallable]] = None,
    message: discord.Message = None,
    page: int = 0,
    timeout: float = 30.0,
) -> _T:
    """
    An emoji-based menu
    .. note:: All pages should be of the same type
    .. note:: All functions for handling what a particular emoji does
              should be coroutines (i.e. :code:`async def`). Additionally,
              they must take all of the parameters of this function, in
              addition to a string representing the emoji reacted with.
              This parameter should be the last one, and none of the
              parameters in the handling functions are optional
    Parameters
    ----------
    ctx: commands.Context
        The command context
    pages: `list` of `str` or `discord.Embed`
        The pages of the menu.
    controls: Optional[Mapping[str, Callable]]
        A mapping of emoji to the function which handles the action for the
        emoji. The signature of the function should be the same as of this function
        and should additionally accept an ``emoji`` parameter of type `str`.
        If not passed, `DEFAULT_CONTROLS` is used *or*
        only a close menu control is shown when ``pages`` is of length 1.
    message: discord.Message
        The message representing the menu. Usually :code:`None` when first opening
        the menu
    page: int
        The current page number of the menu
    timeout: float
        The time (in seconds) to wait for a reaction
    Raises
    ------
    RuntimeError
        If either of the notes above are violated
    """
    if not isinstance(pages[0], (discord.Embed, str)):
        raise RuntimeError("Pages must be of type discord.Embed or str")
    if not all(isinstance(x, discord.Embed) for x in pages) and not all(
        isinstance(x, str) for x in pages
    ):
        raise RuntimeError("All pages must be of the same type")
    if controls is None:
        if len(pages) == 1:
            controls = {"\N{CROSS MARK}": close_menu}
        else:
            controls = DEFAULT_CONTROLS
    for key, value in controls.items():
        maybe_coro = value
        if isinstance(value, functools.partial):
            maybe_coro = value.func
        if not asyncio.iscoroutinefunction(maybe_coro):
            raise RuntimeError("Function must be a coroutine")
    current_page = pages[page]

    if not message:
        if isinstance(current_page, discord.Embed):
            message = await ctx.send(embed=current_page)
        else:
            message = await ctx.send(current_page)
        # Don't wait for reactions to be added (GH-1797)
        # noinspection PyAsyncCall
        start_adding_reactions(message, controls.keys())
    else:
        try:
            if isinstance(current_page, discord.Embed):
                await message.edit(embed=current_page)
            else:
                await message.edit(content=current_page)
        except discord.NotFound:
            return

    try:
        predicates = ReactionPredicate.with_emojis(tuple(controls.keys()), message, ctx.author)
        tasks = [
            asyncio.create_task(ctx.bot.wait_for("reaction_add", check=predicates)),
            asyncio.create_task(ctx.bot.wait_for("reaction_remove", check=predicates)),
        ]
        done, pending = await asyncio.wait(
            tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()

        if len(done) == 0:
            raise asyncio.TimeoutError()
        react, user = done.pop().result()
    except asyncio.TimeoutError:
        if not ctx.me:
            return
        try:
            if (
                isinstance(message.channel, discord.PartialMessageable)
                or message.channel.permissions_for(ctx.me).manage_messages
            ):
                await message.clear_reactions()
            else:
                raise RuntimeError
        except (discord.Forbidden, RuntimeError):  # cannot remove all reactions
            for key in controls.keys():
                try:
                    await message.remove_reaction(key, ctx.bot.user)
                except discord.Forbidden:
                    return
                except discord.HTTPException:
                    pass
        except discord.NotFound:
            return
    else:
        return await controls[react.emoji](
            ctx, pages, controls, message, page, timeout, react.emoji
        )
async def next_page(
    ctx: commands.Context,
    pages: list,
    controls: Mapping[str, _ControlCallable],
    message: discord.Message,
    page: int,
    timeout: float,
    emoji: str,
) -> _T:
    """
    Function for showing next page which is suitable
    for use in ``controls`` mapping that is passed to `menu()`.
    """
    if page >= len(pages) - 1:
        page = 0  # Loop around to the first item
    else:
        page = page + 1
    return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)


async def prev_page(
    ctx: commands.Context,
    pages: list,
    controls: Mapping[str, _ControlCallable],
    message: discord.Message,
    page: int,
    timeout: float,
    emoji: str,
) -> _T:
    """
    Function for showing previous page which is suitable
    for use in ``controls`` mapping that is passed to `menu()`.
    """
    if page <= 0:
        page = len(pages) - 1  # Loop around to the last item
    else:
        page = page - 1
    return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)
async def close_menu(
    ctx: commands.Context,
    pages: list,
    controls: Mapping[str, _ControlCallable],
    message: discord.Message,
    page: int,
    timeout: float,
    emoji: str,
) -> None:
    """
    Function for closing (deleting) menu which is suitable
    for use in ``controls`` mapping that is passed to `menu()`.
    """
    with contextlib.suppress(discord.NotFound):
        await message.delete()
def start_adding_reactions(
    message: discord.Message, emojis: Iterable[_ReactableEmoji]
) -> asyncio.Task:
    """Start adding reactions to a message.
    This is a non-blocking operation - calling this will schedule the
    reactions being added, but the calling code will continue to
    execute asynchronously. There is no need to await this function.
    This is particularly useful if you wish to start waiting for a
    reaction whilst the reactions are still being added - in fact,
    this is exactly what `menu()` uses to do that.
    Parameters
    ----------
    message: discord.Message
        The message to add reactions to.
    emojis : Iterable[Union[str, discord.Emoji]]
        The emojis to react to the message with.
    Returns
    -------
    asyncio.Task
        The task for the coroutine adding the reactions.
    """

    async def task():
        # The task should exit silently if the message is deleted
        with contextlib.suppress(discord.NotFound):
            for emoji in emojis:
                await message.add_reaction(emoji)

    return asyncio.create_task(task())
DEFAULT_CONTROLS: Mapping[str, _ControlCallable] = MappingProxyType(
    {
        "\N{LEFTWARDS BLACK ARROW}\N{VARIATION SELECTOR-16}": prev_page,
        "\N{CROSS MARK}": close_menu,
        "\N{BLACK RIGHTWARDS ARROW}\N{VARIATION SELECTOR-16}": next_page,
    }
)
def error(text: str) -> str:
    """Get text prefixed with an error emoji.
    Parameters
    ----------
    text : str
        The text to be prefixed.
    Returns
    -------
    str
        The new message.
    """
    return f"\N{NO ENTRY SIGN} {text}"


def warning(text: str) -> str:
    """Get text prefixed with a warning emoji.
    Parameters
    ----------
    text : str
        The text to be prefixed.
    Returns
    -------
    str
        The new message.
    """
    return f"\N{WARNING SIGN}\N{VARIATION SELECTOR-16} {text}"
def pagify(
    text: str,
    delims: Sequence[str] = ["\n"],
    *,
    priority: bool = False,
    escape_mass_mentions: bool = True,
    shorten_by: int = 8,
    page_length: int = 2000,
) -> Iterator[str]:
    """Generate multiple pages from the given text.
    Note
    ----
    This does not respect code blocks or inline code.
    Parameters
    ----------
    text : str
        The content to pagify and send.
    delims : `sequence` of `str`, optional
        Characters where page breaks will occur. If no delimiters are found
        in a page, the page will break after ``page_length`` characters.
        By default this only contains the newline.
    Other Parameters
    ----------------
    priority : `bool`
        Set to :code:`True` to choose the page break delimiter based on the
        order of ``delims``. Otherwise, the page will always break at the
        last possible delimiter.
    escape_mass_mentions : `bool`
        If :code:`True`, any mass mentions (here or everyone) will be
        silenced.
    shorten_by : `int`
        How much to shorten each page by. Defaults to 8.
    page_length : `int`
        The maximum length of each page. Defaults to 2000.
    Yields
    ------
    `str`
        Pages of the given text.
    """
    in_text = text
    page_length -= shorten_by
    while len(in_text) > page_length:
        this_page_len = page_length
        if escape_mass_mentions:
            this_page_len -= in_text.count("@here", 0, page_length) + in_text.count(
                "@everyone", 0, page_length
            )
        closest_delim = (in_text.rfind(d, 1, this_page_len) for d in delims)
        if priority:
            closest_delim = next((x for x in closest_delim if x > 0), -1)
        else:
            closest_delim = max(closest_delim)
        closest_delim = closest_delim if closest_delim != -1 else this_page_len
        if escape_mass_mentions:
            to_send = escape(in_text[:closest_delim], mass_mentions=True)
        else:
            to_send = in_text[:closest_delim]
        if len(to_send.strip()) > 0:
            yield to_send
        in_text = in_text[closest_delim:]

    if len(in_text.strip()) > 0:
        if escape_mass_mentions:
            yield escape(in_text, mass_mentions=True)
        else:
            yield in_text