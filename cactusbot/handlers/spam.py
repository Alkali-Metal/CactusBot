"""Handle incoming spam messages."""

from ..handler import Handler
from ..packets import MessagePacket, BanPacket


class SpamHandler(Handler):
    """Spam handler."""

    MAX_SCORE = 16
    MAX_EMOJI = 6
    ALLOW_LINKS = False
    # TODO: Make configurable

    def on_message(self, packet):
        """Handle message events."""

        if packet.role >= 50:  # FIXME: Replace with actual value
            return None

        exceeds_caps = self.check_caps(''.join(
            chunk["text"] for chunk in packet if
            chunk["type"] == "text"
        ))
        exceeds_emoji = self.check_emoji(packet)
        contains_links = self.check_links(packet)

        if exceeds_caps:
            return (MessagePacket("Please do not spam capital letters.",
                                  target=packet.user),
                    BanPacket(packet.user, 1))
        elif exceeds_emoji:
            return (MessagePacket("Please do not spam emoji.",
                                  target=packet.user),
                    BanPacket(packet.user, 1))
        elif contains_links:
            return (MessagePacket("Please do not post links.",
                                  target=packet.user),
                    BanPacket(packet.user, 5))
        else:
            return None

    def check_caps(self, message):
        """Check for excessive capital characters in the message."""
        return sum(char.isupper() - char.islower() for
                   char in message) > self.MAX_SCORE

    def check_emoji(self, packet):
        """Check for excessive emoji in the message."""
        return sum(chunk["type"] == "emoji" for
                   chunk in packet) > self.MAX_EMOJI

    def check_links(self, packet):
        """Check for links in the message."""
        return not self.ALLOW_LINKS and any(
            chunk["type"] == "link" for chunk in packet)
