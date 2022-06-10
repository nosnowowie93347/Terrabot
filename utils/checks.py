from discord.ext import commands
from utils.mysql import *
from utils import config


class owner_only(commands.CommandError):
    pass


class helper_only(commands.CommandError):
    pass


class dev_only(commands.CommandError):
    pass


class support_only(commands.CommandError):
    pass


class not_nsfw_channel(commands.CommandError):
    pass


class not_guild_owner(commands.CommandError):
    pass


class no_permission(commands.CommandError):
    pass


dev_ids = [492883063542513675, 478267562397007873]
supporter_ids = [606284419447128064]


def is_owner():
    def predicate(ctx):
        if ctx.author.id == 466778567905116170:
            return True
        else:
            raise owner_only

    return commands.check(predicate)


def is_helper():
    def predicate(ctx):
        helpers = [503066505999679518]
        if (
            ctx.author.id in helpers
            or ctx.author.id == 466778567905116170
            or ctx.author.id in dev_ids
        ):
            return True
        else:
            raise helper_only

    return commands.check(predicate)


def is_dev():
    def predicate(ctx):
        if ctx.author.id in dev_ids or ctx.author.id == 466778567905116170:
            return True
        else:
            raise dev_only

    return commands.check(predicate)


def is_support():
    def predicate(ctx):
        if (
            ctx.author.id in support_ids
            or ctx.author.id in dev_ids
            or ctx.author.id == 466778567905116170
        ):
            return True
        else:
            raise support_only

    return commands.check(predicate)


def is_nsfw_channel():
    def predicate(ctx):
        if not isinstance(ctx.channel, discord.DMChannel) and ctx.channel.is_nsfw():
            return True
        else:
            raise not_nsfw_channel

    return commands.check(predicate)


def is_guild_owner():
    def predicate(ctx):
        if ctx.author.id == ctx.guild.owner_id:
            return True
        else:
            raise not_guild_owner

    return commands.check(predicate)


def server_mod_or_perms(**permissions):
    def predicate(ctx):
        if not ctx.guild:
            return True
        mod_role_name = read_data_entry(ctx.guild.id, "mod-role")
        mod = discord.utils.get(ctx.author.roles, name=mod_role_name)
        if (
            mod
            or permissions
            and all(
                getattr(ctx.channel.permissions_for(ctx.author), name, None) == value
                for name, value in permissions.items()
            )
        ):
            return True
        else:
            raise no_permission

    return commands.check(predicate)


def has_permissions(**permissions):
    def predicate(ctx):
        if all(
            getattr(ctx.channel.permissions_for(ctx.author), name, None) == value
            for name, value in permissions.items()
        ):
            return True
        else:
            raise no_permission

    return commands.check(predicate)
