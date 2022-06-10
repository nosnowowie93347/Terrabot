import discord
import logging

from discord.ext import commands

from safemodels import SafeGuild, SafeMember, SafeRole


class MassDM(commands.Cog):
    """Send a direct message to all members of the specified Role."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["mdm"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def massdm(
        self, ctx: commands.Context, role: discord.Role, *, message: str
    ) -> None:
        """Sends a DM to all Members with the given Role.
        Allows for the following customizations:
          `{member}` is the member being messaged
          `{role}` is the role through which they are being messaged
          `{server}` is the server through which they are being messaged
          `{sender}` is you, the person sending the message
        """

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            log.warning("Failed to delete command message: insufficient permissions")
        except discord.DiscordException:
            log.warning("Failed to delete command message")

        for member in [m for m in role.members if not m.bot]:
            try:
                await member.send(
                    message.format(
                        member=SafeMember(member),
                        role=SafeRole(role),
                        server=SafeGuild(ctx.guild),
                        guild=SafeGuild(ctx.guild),
                        sender=SafeMember(ctx.author),
                    )
                )
            except discord.Forbidden:
                log.warning(
                    f"Failed to DM user {member} (ID {member.id}): insufficient permissions"
                )
                continue
            except discord.DiscordException:
                log.warning(f"Failed to DM user {member} (ID {member.id})")
                continue


def setup(bot):
    bot.add_cog(MassDM(bot))
