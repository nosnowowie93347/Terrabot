import discord, random, asyncio, math, aiohttp, json
from random import choice, randint, randrange
from discord.ext import commands
from cogs.utils.test import error

emojilist = open("Emojis.txt", encoding="utf8").read().splitlines()


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(json_serialize=json.dumps)

    @commands.command(name="createemoji")
    async def emoji_add(self, ctx, name: str, url: str, *roles: discord.Role):
        """Create custom emoji
        Use double quotes if role name has spaces
        Examples:
                `[p]emoji add Example https://example.com/image.png`
                `[p]emoji add RoleBased https://example.com/image.png EmojiRole "Test image"`
        """
        try:
            async with self.session.get(url) as r:
                data = await r.read()
        except Exception as e:
            await ctx.send(
                error(("Unable to get emoji from provided url: {}").format(e))
            )
            return
        try:
            await ctx.guild.create_custom_emoji(
                name=name,
                image=data,
                roles=roles,
                reason=("Restricted to roles: {}").format(
                    ", ".join(role.name for role in roles)
                )
                if roles
                else None,
            )

        except discord.InvalidArgument:
            await ctx.send(
                error(("This image type is unsupported, or link is incorrect"))
            )
        except discord.HTTPException as e:
            await ctx.send(error(("An error occured on adding an emoji: {}").format(e)))
        else:
            await ctx.send("Success.")

    @commands.command()
    async def emojify(self, ctx, *, text: str):
        """
        Converts the alphabet and spaces into emoji
        """
        author = ctx.message.author
        emojified = "⬇ Copy and paste this: ⬇\n"
        formatted = re.sub(r"[^A-Za-z ]+", "", text).lower()
        if text == "":
            await ctx.send("Remember to say what you want to convert!")
        else:
            for i in formatted:
                if i == " ":
                    emojified += "     "
                else:
                    emojified += ":regional_indicator_{}: ".format(i)
            if len(emojified) + 2 >= 2000:
                await ctx.send("Your message in emojis exceeds 2000 characters!")
            if len(emojified) <= 25:
                await ctx.send("Your message could not be converted!")
            else:
                await ctx.send("`" + emojified + "`")

    # Get emotes from all servers
    @commands.command(
        aliases=["emoji", "emojis"],
        description="Displays all emotes avaiable on a server.",
    )
    async def emotes(self, ctx):

        embed = discord.Embed(
            title="Emojis",
            description="Here are all the emojis available on the servers with Terrabot:",
            color=0x00FF00,
        )  # setup embed

        for ej in ctx.message.guild.emojis:
            output = ej
            # Here we need 2 strings to add the backtick styling and avoid "too many arguments" errors
            output2 = "```{}```".format(str(output))
            # Add info to list (embed)
            embed.add_field(name=ej.name, value=output2, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def randomemoji(self, ctx):
        """get a random emoji"""
        await ctx.send(random.choice(emojilist))


def setup(bot):
    bot.add_cog(Emoji(bot))
