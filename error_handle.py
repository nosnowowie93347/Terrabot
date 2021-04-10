import contextlib, logging, asyncio, aiohttp
from urllib.parse import quote as quote_url
import typing as t
from typing import Optional, List, Hashable
from discord import Embed
from discord.ext.commands import Cog, Context, errors
from sentry_sdk import push_scope
log = logging.getLogger("discord")
class LockedResourceError(RuntimeError):
	"""
	Exception raised when an operation is attempted on a locked resource.
	Attributes:
		`type` -- name of the locked resource's type
		`id` -- ID of the locked resource
	"""

	def __init__(self, resource_type: str, resource_id: Hashable):
		self.type = resource_type
		self.id = resource_id

		super().__init__(
			f"Cannot operate on {self.type.lower()} `{self.id}`; "
			"it is currently locked and in use by another operation."
		)
class ResponseCodeError(ValueError):
	"""Raised when a non-OK HTTP response is received."""

	def __init__(
		self,
		response: aiohttp.ClientResponse,
		response_json: Optional[dict] = None,
		response_text: str = ""
	):
		self.status = response.status
		self.response_json = response_json or {}
		self.response_text = response_text
		self.response = response

	def __str__(self):
		response = self.response_json if self.response_json else self.response_text
		return f"Status: {self.status} Response: {response}"
class ErrorHandler(Cog):
	"""Handles errors emitted from commands."""

	def __init__(self, bot):
		self.bot = bot

	def _get_error_embed(self, title: str, body: str) -> Embed:
		"""Return an embed that contains the exception."""
		return Embed(
			title=title,
			colour=0x676767,
			description=body
		)

	@Cog.listener()
	async def on_command_error(self, ctx: Context, e: errors.CommandError) -> None:
		"""
		Provide generic command error handling.
		Error handling is deferred to any local error handler, if present. This is done by
		checking for the presence of a `handled` attribute on the error.
		Error handling emits a single error message in the invoking context `ctx` and a log message,
		prioritised as follows:
		1. If the name fails to match a command:
			* If it matches shh+ or unshh+, the channel is silenced or unsilenced respectively.
			  Otherwise if it matches a tag, the tag is invoked
			* If CommandNotFound is raised when invoking the tag (determined by the presence of the
			  `invoked_from_error_handler` attribute), this error is treated as being unexpected
			  and therefore sends an error message
			* Commands in the verification channel are ignored
		2. UserInputError: see `handle_user_input_error`
		3. CheckFailure: see `handle_check_failure`
		4. CommandOnCooldown: send an error message in the invoking context
		5. ResponseCodeError: see `handle_api_error`
		6. Otherwise, if not a DisabledCommand, handling is deferred to `handle_unexpected_error`
		"""
		command = ctx.command

		if hasattr(e, "handled"):
			log.trace(f"Command {command} had its error already handled locally; ignoring.")
			return

		if isinstance(e, errors.CommandNotFound):
			await ctx.send("Oops! This command doesn't exist. If you think it should, dm the devs with ur suggestion.")
			return
		elif isinstance(e, errors.NotOwner):
			await ctx.send("ERROR: " + e)
			return
		elif isinstance(e, errors.UserInputError):
			await self.handle_user_input_error(ctx, e)
		elif isinstance(e, errors.CheckFailure):
			await self.handle_check_failure(ctx, e)
		elif isinstance(e, errors.CommandOnCooldown):
			await ctx.send(e)
		elif isinstance(e, errors.CommandInvokeError):
			if isinstance(e.original, ResponseCodeError):
				await self.handle_api_error(ctx, e.original)
			elif isinstance(e.original, LockedResourceError):
				await ctx.send(f"{e.original} Please wait for it to finish and try again later.")
			else:
				await self.handle_unexpected_error(ctx, e.original)
			return  # Exit early to avoid logging.
		elif not isinstance(e, errors.DisabledCommand):
			# ConversionError, MaxConcurrencyReached, ExtensionError
			await self.handle_unexpected_error(ctx, e)
			return  # Exit early to avoid logging.

		log.debug(
			f"Command {command} invoked by {ctx.message.author} with error "
			f"{e.__class__.__name__}: {e}"
		)

	@staticmethod
	def get_help_command(ctx: Context) -> t.Coroutine:
		"""Return a prepared `help` command invocation coroutine."""
		if ctx.command:
			return ctx.send_help(ctx.command)

		return ctx.send_help()

   

	async def handle_user_input_error(self, ctx: Context, e: errors.UserInputError) -> None:
		"""
		Send an error message in `ctx` for UserInputError, sometimes invoking the help command too.
		* MissingRequiredArgument: send an error message with arg name and the help command
		* TooManyArguments: send an error message and the help command
		* BadArgument: send an error message and the help command
		* BadUnionArgument: send an error message including the error produced by the last converter
		* ArgumentParsingError: send an error message
		* Other: send an error message and the help command
		"""
		prepared_help_command = self.get_help_command(ctx)

		if isinstance(e, errors.MissingRequiredArgument):
			embed = self._get_error_embed("Missing required argument", e.param.name)
			await ctx.send(embed=embed)
			await prepared_help_command
		elif isinstance(e, errors.TooManyArguments):
			embed = self._get_error_embed("Too many arguments", str(e))
			await ctx.send(embed=embed)
			await prepared_help_command
		elif isinstance(e, errors.BadArgument):
			embed = self._get_error_embed("Bad argument", str(e))
			await ctx.send(embed=embed)
			await prepared_help_command
		elif isinstance(e, errors.BadUnionArgument):
			embed = self._get_error_embed("Bad argument", f"{e}\n{e.errors[-1]}")
			await ctx.send(embed=embed)
		elif isinstance(e, errors.ArgumentParsingError):
			embed = self._get_error_embed("Argument parsing error", str(e))
			await ctx.send(embed=embed)
		else:
			embed = self._get_error_embed(
				"Input error",
				"Something about your input seems off. Check the arguments and try again."
			)
			await ctx.send(embed=embed)
			await prepared_help_command

	@staticmethod
	async def handle_check_failure(ctx: Context, e: errors.CheckFailure) -> None:
		"""
		Send an error message in `ctx` for certain types of CheckFailure.
		The following types are handled:
		* BotMissingPermissions
		* BotMissingRole
		* BotMissingAnyRole
		* NoPrivateMessage
		* InWhitelistCheckFailure
		"""
		bot_missing_errors = (
			errors.BotMissingPermissions,
			errors.BotMissingRole,
			errors.BotMissingAnyRole
		)

		if isinstance(e, bot_missing_errors):
			await ctx.send(
				"Sorry, it looks like I don't have the permissions or roles I need to do that."
			)
		elif isinstance(e, (errors.NoPrivateMessage)):
			await ctx.send(e)
		elif isinstance(e, (errors.PrivateMessageOnly)):
			await ctx.send(e)
		elif isinstance(e, (errors.MissingPermissions)):
			await ctx.send("ERROR: YOU DO NOT HAVE PERMISSION TO USE THIS COMMAND.")

	@staticmethod
	async def handle_api_error(ctx: Context, e: ResponseCodeError) -> None:
		"""Send an error message in `ctx` for ResponseCodeError and log it."""
		if e.status == 404:
			await ctx.send("There does not seem to be anything matching your query.")
			log.debug(f"API responded with 404 for command {ctx.command}")
		elif e.status == 400:
			content = await e.response.json()
			log.debug(f"API responded with 400 for command {ctx.command}: %r.", content)
			await ctx.send("According to the API, your request is malformed.")
		elif 500 <= e.status < 600:
			await ctx.send("Gosh dangit. Looks like the API made a fucky wucky and broke.")
			log.warning(f"API responded with {e.status} for command {ctx.command}")
		else:
			await ctx.send(f"Got an unexpected status code from the API (`{e.status}`).")
			log.warning(f"Unexpected API response for command {ctx.command}: {e.status}")

	@staticmethod
	async def handle_unexpected_error(ctx: Context, e: errors.CommandError) -> None:
		"""Send a generic error message in `ctx` and log the exception as an error with exc_info."""
		await ctx.send(
			f"Sorry, an unexpected error occurred. Please let us know!\n\n"
			f"```{e.__class__.__name__}: {e}```"
		)


		with push_scope() as scope:
			scope.user = {
				"id": ctx.author.id,
				"username": str(ctx.author)
			}

			scope.set_tag("command", ctx.command.qualified_name)
			scope.set_tag("message_id", ctx.message.id)
			scope.set_tag("channel_id", ctx.channel.id)

			scope.set_extra("full_message", ctx.message.content)

			if ctx.guild is not None:
				scope.set_extra(
					"jump_to",
					f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"
				)

			log.error(f"Error executing command invoked by {ctx.message.author}: {ctx.message.content}", exc_info=e)


def setup(bot):
	"""Load the ErrorHandler cog."""
	bot.add_cog(ErrorHandler(bot))
