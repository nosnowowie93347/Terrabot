from common_variables import TWEMOJI_URL


async def get_twemoji(emoji: str):
    emoji_unicode = []
    for char in emoji:
        char = hex(ord(char))[2:]
        emoji_unicode.append(char)
    if "200d" not in emoji_unicode:
        emoji_unicode = list(filter(lambda c: c != "fe0f", emoji_unicode))
    emoji_unicode = "-".join(emoji_unicode)
    return f"{TWEMOJI_URL}/{emoji_unicode}.png"


def inline(text: str) -> str:
    """Get the given text as inline code.
    Parameters
    ----------
    text : str
        The text to be marked up.
    Returns
    -------
    str
        The marked up text.
    """
    if "`" in text:
        return f"``{text}``"
    else:
        return f"`{text}`"
