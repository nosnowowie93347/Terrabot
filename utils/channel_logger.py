import discord
import time

from utils.logger import log
channel_logger_id = None
log_time_format = "%H:%M:%S"
log_date_format = "%m-%d-%Y"
class Channel_Logger():
    def __init__(self, bot):
        self.bot = bot

    async def log_to_channel(self, msg):
        if channel_logger_id:
            channel = self.bot.get_channel(int(channel_logger_id))
            if not channel:
                log.warning("Can't find logging channel")
            else:
                try:
                    await channel.send(":stopwatch: `{}` {}".format(time.strftime(log_time_format), msg))
                except discord.errors.Forbidden:
                    log.warning("Could not log to the channel log channel because I do not have permission to send messages in it!")
