"""Handle events"""

import datetime

from ..cached import CacheUtils
from ..handler import Handler


class EventHandler(Handler):
    """Events handler."""

    def __init__(self, cache_data):
        super().__init__()

        self.cache = CacheUtils("caches/followers.json")
        self.cache_follows = cache_data["CACHE_FOLLOWS"]
        self.follow_time = datetime.timedelta(
            minutes=cache_data["CACHE_FOLLOWS_TIME"])

    async def on_follow(self, packet):
        """Handle follow packets."""

        # TODO: Make configurable
        response = "Thanks for following, @{} !".format(packet.user)

        if packet.success:
            if self.cache_follows:
                now = datetime.datetime.utcnow()
                if packet.user in self.cache:
                    cache_time = self.cache[packet.user]
                    if cache_time + self.follow_time <= now:
                        self.cache[packet.user] = now.isoformat()
                        return response
                else:
                    self.cache[packet.user] = now.isoformat()
                    return response
            else:
                return response

    async def on_subscribe(self, packet):
        """Handle subscription packets."""
        # TODO: Make configurable
        return "Thanks for subscribing, @{} !".format(packet.user)

    async def on_host(self, packet):
        """Handle host packets."""
        # TODO: Make configurable
        return "Thanks for hosting, @{} !".format(packet.user)
