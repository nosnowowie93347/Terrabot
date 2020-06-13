import asyncio, discord
from   discord.ext import commands
from   Cogs        import Nullify, DisplayName, UserTime, Message, PickList
def setup(bot):
    # Add the bot and deps
    settings = bot.get_cog("Settings")
    bot.add_cog(ServerStats(bot, settings))

class ServerStats(commands.Cog):

    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        global Utils, DisplayName

    @commands.command()
    async def recentjoins(self, ctx):
        """Lists the most recent users to join."""
        our_list = []
        # offset = self.settings.getGlobalUserStat(ctx.author,"TimeZone",self.settings.getGlobalUserStat(ctx.author,"UTCOffset",None))
        for member in ctx.guild.members:
            our_list.append(
                {
                    "name":member.name,
                    "value":"{} UTC".format(member.joined_at.strftime("%Y-%m-%d %I:%M %p") if member.joined_at != None else "Unknown"),#UserTime.getUserTime(ctx.author,self.settings,member.joined_at,force=offset)["vanity"],
                    "date":member.joined_at
                }
            )
        our_list = sorted(our_list, key=lambda x:x["date"].timestamp() if x["date"] != None else -1)
        return await PickList.PagePicker(title="Most Recent Members to Join {} ({:,} total)".format(ctx.guild.name,len(ctx.guild.members)),ctx=ctx,list=[{"name":"{}. {}".format(y+1,x["name"]),"value":x["value"]} for y,x in enumerate(our_list)]).pick()
        