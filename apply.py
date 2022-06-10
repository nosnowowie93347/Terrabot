import discord, asyncio, random, json, datetime, time
from discord import ext, utils
from discord.ext import commands


class ApplyNow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def applymod(self, ctx, member: discord.Member = None):
        owner = self.bot.get_user(466778567905116170)

        """`Apply for Moderator (Testing)`"""

        member = ctx.author if not member else member

        def checkmsg(m):
            return m.author == member

        def checkreact(reaction, user):
            return user.id == member.id and str(reaction.emoji) in ["✅", "❌"]

        try:
            doodoo = discord.Embed(
                title="Application will start soon...",
                description="Remember to be 100% Honest and provide good answers!\nThe Questions will be sent shortly...",
                color=discord.Color.dark_orange(),
            )
            await member.send(embed=doodoo)
            async with member.typing():
                await asyncio.sleep(5)
            await member.send("What's your Minecraft IGN + Discord Username?")
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            first = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send(
                "How old are you? (If you feel uncomfortable saying this, just confirm if you're at least a teenager)"
            )
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            second = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send(
                "What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)"
            )
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            third = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send(
                "Why do you want to be Moderator? Isn't it fun to play without any responsibilites?"
            )
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            fourth = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("What will you do for the Discord Server?")
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            fifth = msg.content
            async with member.typing():
                await asyncio.sleep(2)
            await member.send("Anything else you want to say?")
            msg = await self.bot.wait_for("message", check=checkmsg, timeout=250.0)
            sixth = msg.content

        except asyncio.TimeoutError:
            await member.send("You took too long to write in a response :(")
        else:
            poo = await member.send("Are you sure you want to submit this application?")
            await poo.add_reaction("✅")
            await poo.add_reaction("❌")
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=checkreact
            )
            if str(reaction.emoji) == "✅":
                async with member.typing():
                    await asyncio.sleep(3)
                await member.send(
                    "Thank you for applying! Your application will be sent to the Owner soon"
                )
                await asyncio.sleep(3)
                poopoo = discord.Embed(
                    title="Application Answers",
                    description=f"1) What's your Minecraft IGN + Discord Username?\n{first}, \n2) How old are you? (If you're not comfortable saying this at least confirm if you're a teenager)\n{second}, \n3) What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)\n{third}, \n4)Why do you want to be Moderator? Isn't it fun to play without any responsibilites?\n{fourth}, \n5) What will you do for the Discord Server?\n{fifth}, \n6) Anything else you want to say?\n{sixth}",
                    color=discord.Color.dark_orange(),
                )
                poopoo.set_author(
                    name=f"Application taken by: {member}",
                    icon_url=f"{member.avatar_url}",
                )
                poopoo.set_footer(text=f"{member}")
                poopoo.timestamp = datetime.datetime.utcnow()
                await owner.send(embed=poopoo)
            else:
                if str(reaction.emoji) == "❌":
                    await member.send("Application won't be sent")


def setup(bot):
    bot.add_cog(ApplyNow(bot))
