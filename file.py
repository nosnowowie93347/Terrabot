import yaml, discord, logging
from typing import Dict, Iterable, List, Set
log = logging.getLogger(__name__)

with open("config-default.yml", encoding="UTF-8") as f:
	_CONFIG_YAML = yaml.safe_load(f)
class YAMLGetter(type):
	"""
	Implements a custom metaclass used for accessing
	configuration data by simply accessing class attributes.
	Supports getting configuration from up to two levels
	of nested configuration through `section` and `subsection`.
	`section` specifies the YAML configuration section (or "key")
	in which the configuration lives, and must be set.
	`subsection` is an optional attribute specifying the section
	within the section from which configuration should be loaded.
	Example Usage:
		# config.yml
		bot:
			prefixes:
				direct_message: ''
				guild: '!'
		# config.py
		class Prefixes(metaclass=YAMLGetter):
			section = "bot"
			subsection = "prefixes"
		# Usage in Python code
		from config import Prefixes
		def get_prefix(bot, message):
			if isinstance(message.channel, PrivateChannel):
				return Prefixes.direct_message
			return Prefixes.guild
	"""

	subsection = None

	def __getattr__(cls, name):
		name = name.lower()

		try:
			if cls.subsection is not None:
				return _CONFIG_YAML[cls.section][cls.subsection][name]
			return _CONFIG_YAML[cls.section][name]
		except KeyError:
			dotted_path = '.'.join(
				(cls.section, cls.subsection, name)
				if cls.subsection is not None else (cls.section, name)
			)
			log.critical(f"Tried accessing configuration variable at `{dotted_path}`, but it could not be found.")
			raise

	def __getitem__(cls, name):
		return cls.__getattr__(name)

	def __iter__(cls):
		"""Return generator of key: value pairs of current constants class' config values."""
		for name in cls.__annotations__:
			yield name, getattr(cls, name)    
class AntiSpam(metaclass=YAMLGetter):
	section = 'anti_spam'

	clean_offending: bool
	ping_everyone: bool

	punishment: Dict[str, Dict[str, int]]
	rules: Dict[str, Dict[str, int]]
class Filter(metaclass=YAMLGetter):
	section = "filter"

	filter_zalgo: bool
	filter_invites: bool
	filter_domains: bool
	filter_everyone_ping: bool
	watch_regex: bool
	watch_rich_embeds: bool

	# Notifications are not expected for "watchlist" type filters
	notify_user_zalgo: bool
	notify_user_invites: bool
	notify_user_domains: bool
	notify_user_everyone_ping: bool

	ping_everyone: bool
	offensive_msg_delete_days: int

	
class Guild(metaclass=YAMLGetter):
    section = "guild"

    id: int
    invite: str  # Discord invite, gets embedded in chat
    moderation_channels: List[int]
    moderation_categories: List[int]
    moderation_roles: List[int]
    modlog_blacklist: List[int]
    reminder_whitelist: List[int]
    staff_roles: List[int]