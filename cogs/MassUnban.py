import asyncio
import discord
from discord.ext import commands
from .utils.test2 import MessagePredicate


class MassUnban(commands.Cog):
    """Unban all users, or users with a specific ban reason."""

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def massunban(self, ctx, *, ban_reason = None):
        """
        Mass unban everyone, or specific people.
        
        `ban_reason` is what the bot looks for in the original ban reason to qualify a user for an unban. It is case-insensitive.
        """
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            msg = "I need the `Ban Members` permission to fetch the ban list for the guild."
            await ctx.send(msg)
            return

        bancount = len(banlist)
        if bancount == 0:
            await ctx.send("No users are banned from this server.")
            return

        unban_count = 0
        if not ban_reason:
            warning_string = (
                "Are you sure you want to unban every banned person on this server?\n"
                f"**Please read** `{ctx.prefix}help massunban` **as this action can cause a LOT of modlog messages!**\n"
                "Type `Yes` to confirm, or `No` to cancel."
            )
            await ctx.send(warning_string)
            pred = MessagePredicate.yes_or_no(ctx)
            try:
                await self.bot.wait_for("message", check=pred, timeout=15)
                if pred.result is True:
                    async with ctx.typing():
                        for ban_entry in banlist:
                            await ctx.guild.unban(ban_entry.user, reason=f"Mass Unban requested by {str(ctx.author)} ({ctx.author.id})")
                            await asyncio.sleep(0.5)
                            unban_count += 1
                else:
                    return await ctx.send("Alright, I'm not unbanning everyone.")
            except asyncio.TimeoutError:
                return await ctx.send("Response timed out. Please run this command again if you wish to try again.")
        else:
            async with ctx.typing():
                for ban_entry in banlist:
                    if not ban_entry.reason:
                        continue
                    if ban_reason.lower() in ban_entry.reason.lower():
                        await ctx.guild.unban(ban_entry.user, reason=f"Mass Unban requested by {str(ctx.author)} ({ctx.author.id})")
                        await asyncio.sleep(0.5)
                        unban_count += 1

        await ctx.send(f"Done. Unbanned {unban_count} users.")
def setup(bot):
    bot.add_cog(MassUnban(bot))