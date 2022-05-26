import asyncio, discord
import datetime
import logging
from discord import Emoji, Colour
from typing import Any, Dict, Final, List, Optional, Tuple, TypeVar
from discord.ext import commands
from discord.ext.commands import Bot
import aiohttp



_config_structure: Final[Dict[str, Any]] = {
    "custom_url": "https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927",
    "image_url": "https://cdn.discordapp.com/icons/798037520562126848/b0d7d3a653199cae56530ffbddaf1a98.webp?size=1024",
    "custom_message": "Here's the link to invite me to your server!!: https://bit.ly/3LNHTIB",
    "send_in_channel": True,
    "embeds": True,
    "title": "Invite {bot_name}",
    "support_server": None,
    "footer": "Terrabot",
    "extra_link": False,
    "support_server_emoji": {},
    "invite_emoji": {"<:institute:977005054122917938>"},
}
class AdvancedInvite(commands.Cog):
    """An advanced invite for [botname]
    """

    def __init__(self, bot):
        self.bot = bot
        self._invite_command: Optional[commands.Command] = self.bot.remove_command("invite")
       
        self._supported_images: Tuple[str, ...] = ("jpg", "jpeg", "png", "gif")


    @commands.command(name="invite", usage="")
    @commands.guild_only()
    async def invite(self, ctx: commands.Context, send_in_channel: Optional[bool] = False):
        """Invite [botname] to your server!"""

        channel = ctx.channel
        title = _config_structure["title"].replace(
            "{bot_name}", ctx.me.name
        )
        message = _config_structure["custom_message"]
        url = "https://discord.com/oauth2/authorize?client_id=657372691749273612&scope=bot&permissions=2134375927"
        time = datetime.datetime.now(tz=datetime.timezone.utc)
        footer = _config_structure["footer"]
        
        timestamp = f"<t:{int(time.timestamp())}>"
        support = _config_structure["support_server"]
        support_msg = f"\nJoin the support server! <{support}>\n" if support is not None else ""
        kwargs: Dict[str, Any] = {
            "content": f"**{title}**\n{message}\n<{url}>{support_msg}\n\n{footer}\n{timestamp}"
        }

        support_server_emoji = _config_structure["support_server_emoji"]
        invite_emoji = _config_structure["invite_emoji"]

        embed = discord.Embed(
            title=title,
            description=message,
            colour=Colour.random(),
            timestamp=time,
        )
        if support is not None:
            embed.add_field(name="Join the support server", value=support)

        if iurl := _config_structure["image_url"]:
            embed.set_image(url=iurl)
        if footer:
            embed.set_footer(text=footer)

        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.reply("I could not dm you!")
def setup(bot):
    bot.add_cog(AdvancedInvite(bot))