"""Interact with Mixer chat."""

import itertools
import json
import logging

from .. import WebSocket


class MixerChat(WebSocket):
    """Interact with Mixer chat."""

    def __init__(self, channel, *endpoints):
        super().__init__(*endpoints)

        self.logger = logging.getLogger(__name__)

        assert isinstance(channel, int), "Channel ID must be an integer."
        self.channel = channel

        self._packet_counter = itertools.count()

    async def send(self, *args, max_length=360, **kwargs):
        """Send a packet."""

        packet = {
            "type": "method",
            "method": "msg",
            "arguments": args,
            "id": kwargs.get("id") or self._packet_id
        }

        packet.update(kwargs)

        if packet["method"] in ("msg", "whisper"):

            message = packet.copy()["arguments"][-1]

            for index in range(0, len(message), max_length):

                chunk = message[index:index + max_length]
                packet["arguments"] = (*packet["arguments"][:-1], chunk)

                await self._send(json.dumps(packet))

        else:
            await self._send(json.dumps(packet))

    async def initialize(self, *auth):
        """Send an authentication packet."""
        if auth:
            user_id, get_chat = auth
            authkey = (await get_chat())["authkey"]
            await self.send(self.channel, user_id, authkey, method="auth")
        else:
            await self.send(self.channel, method="auth")

    parse = WebSocket._parse_json()

    @property
    def _packet_id(self):
        return next(self._packet_counter)