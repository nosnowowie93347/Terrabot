import logging, re, discord

from discord import Colour, Message, NotFound
from discord.ext.commands import Cog, Bot

WEBHOOK_URL_RE = re.compile(
    r"((?:https?://)?discord(?:app)?\.com/api/webhooks/\d+/)\S+/?", re.IGNORECASE
)

ALERT_MESSAGE_TEMPLATE = (
    "{user}, looks like you posted a Discord webhook URL. Therefore, your "
    "message has been removed. Your webhook may have been **compromised** so "
    "please re-create the webhook **immediately**. If you believe this was "
    "mistake, please let us know."
)

log = logging.getLogger(__name__)


def format_user(user: discord.abc.User) -> str:
    """Return a string for `user` which has their mention and ID."""
    return f"{user.mention} (`{user.id}`)"


class WebhookRemover(Cog):
    """Scan messages to detect Discord webhooks links."""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def delete_and_respond(self, msg: Message, redacted_url: str) -> None:
        """Delete `msg` and send a warning that it contained the Discord webhook `redacted_url`."""
        # Don't log this, due internal delete, not by user. Will make different entry.

        try:
            await msg.delete()
        except NotFound:
            log.debug(
                f"Failed to remove webhook in message {msg.id}: message already deleted."
            )
            return

        await msg.channel.send(ALERT_MESSAGE_TEMPLATE.format(user=msg.author.mention))

        message = (
            f"{format_user(msg.author)} posted a Discord webhook URL to {msg.channel.mention}. "
            f"Webhook URL was `{redacted_url}`"
        )
        log.debug(message)

    @Cog.listener()
    async def on_message(self, msg: Message) -> None:
        """Check if a Discord webhook URL is in `message`."""
        # Ignore DMs; can't delete messages in there anyway.
        if not msg.guild or msg.author.bot:
            return

        matches = WEBHOOK_URL_RE.search(msg.content)
        if matches:
            await self.delete_and_respond(msg, matches[1] + "xxx")

    @Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Check if a Discord webhook URL is in the edited message `after`."""
        await self.on_message(after)


def setup(bot: Bot) -> None:
    """Load `WebhookRemover` cog."""
    bot.add_cog(WebhookRemover(bot))
