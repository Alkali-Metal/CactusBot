import pytest

from cactusbot.handlers import SpamHandler
from cactusbot.packets import MessagePacket

spam_handler = SpamHandler()


class TestSpamHandler:

    @pytest.mark.asyncio
    async def test_on_message(self):
        assert await spam_handler.on_message(MessagePacket(
            "PLEASE STOP SPAMMING CAPITAL LETTERS.",
            role=50
        )) is None

        assert (await spam_handler.on_message(MessagePacket(
            "THIS CONTAINS EXCESSIVE CAPITAL LETTERS."
        )))[0].text == "Please do not spam capital letters."

        assert (await spam_handler.on_message(MessagePacket(
            "This is what one hundred emoji looks like!",
            *(("emoji", ":open_mouth:"),) * 100
        )))[0].text == "Please do not spam emoji."

        assert (await spam_handler.on_message(MessagePacket(
            "Check out my amazing Twitter!",
            ("link", "twitter.com/CactusDevTeam",
             "https://twitter.com/CactusDevTeam")
        )))[0].text == "Please do not post links."

    def test_check_caps(self):
        assert not spam_handler.check_caps("")
        assert not spam_handler.check_caps("3.14159265358979")

        assert not spam_handler.check_caps("This is a reasonable message!")
        assert not spam_handler.check_caps("WOW, that was incredible!")

        assert spam_handler.check_caps("THIS IS DEFINITELY CAPITALIZED SPAM.")
        assert spam_handler.check_caps("THAT was SO COOL! OMG WOW FANTASTIC!")

    def test_check_emoji(self):
        assert not spam_handler.check_emoji(MessagePacket(
            "This message contains no emoji."
        ))

        assert not spam_handler.check_emoji(MessagePacket(
            "Wow, that was great!",
            ("emoji", ":smile:")
        ))

        assert not spam_handler.check_emoji(MessagePacket(
            *(("emoji", ":cactus:"),) * 6
        ))

        assert not spam_handler.check_emoji(MessagePacket(
            ("emoji", ":smiley:"),
            ("emoji", ":stuck_out_tongue:"),
            ("emoji", ":cactus:"),
            ("emoji", ":hamster:"),
            ("emoji", ":potato:"),
            ("emoji", ":green_heart:")
        ))

        assert spam_handler.check_emoji(MessagePacket(
            *(("emoji", ":cactus:"),) * 7
        ))

        assert spam_handler.check_emoji(MessagePacket(
            ("emoji", ":smiley:"),
            ("emoji", ":stuck_out_tongue:"),
            ("emoji", ":cactus:"),
            ("emoji", ":hamster:"),
            ("emoji", ":potato:"),
            ("emoji", ":green_heart:"),
            ("emoji", ":sunglasses:")
        ))

        assert spam_handler.check_emoji(MessagePacket(
            *(("emoji", ":smile:"),) * 100
        ))

    def test_check_links(self):
        assert not spam_handler.check_links(MessagePacket(
            "This message contains no links."
        ))

        assert not spam_handler.check_links(MessagePacket(
            "google.com was not parsed as a link, and is therefore 'fine'."
        ))

        assert spam_handler.check_links(MessagePacket(
            "You should go check out ",
            ("link", "cactusbot.rtfd.org", "https://cactusbot.rtfd.org")
        ))
