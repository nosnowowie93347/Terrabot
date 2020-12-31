import yaml, discord, logging
with open("config-default.yml", encoding="UTF-8") as f:
    _CONFIG_YAML = yaml.safe_load(f)    
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

    channel_whitelist: None