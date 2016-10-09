"""Cube things."""

import re

from random import choice
from difflib import get_close_matches

from . import Command
from ...packets import MessagePacket
from ...services.beam.parser import BeamParser


class Cube(Command):
    """Cube things."""

    COMMAND = "cube"

    NUMBER_EXPR = re.compile(r'^[-+]?\d*\.\d+|[-+]?\d+$')

    @Command.subcommand(hidden=True)
    async def run(self, *args: False, username: "username") -> "cube":
        """Cube things!"""

        if not args:
            return self.cube(username)
        if args == ('2',):
            return MessagePacket("8. Woah, that's 2Cubed!")
        elif len(args) > 8:
            return MessagePacket("Woah, that's 2 many cubes")

        return MessagePacket(' · '.join(self.cube(arg).text for arg in args))

    def cube(self, value: str):
        """Cube a value."""

        if value.startswith(':'):  # HACK: global emote parsing required
            return '{} ³'.format(value)

        match = re.match(self.NUMBER_EXPR, value)
        if match is not None:
            return MessagePacket('{:.4g}'.format(float(match.string)**3))
        return MessagePacket('({})³'.format(value))

    DEFAULT = run


class Temmie(Command):
    "awwAwa!!"

    COMMAND = "temmie"

    QUOTES = (
        ("fhsdhjfdsfjsddshjfsd", False),
        ("hOI!!!!!! i'm tEMMIE!!", False),
        ("awwAwa cute!! (pets u)", False),
        ("OMG!! humans TOO CUTE (dies)", False),
        ("NO!!!!! muscles r... NOT CUTE", False),
        ("NO!!! so hungr... (dies)", False),
        ("FOOB!!!", False),
        ("can't blame a BARK for tryin'...", False),
        ("RATED TEM OUTTA TEM. Loves to pet cute humans. "
         "But you're allergic!", True),
        ("Special enemy Temmie appears here to defeat you!!", True),
        ("Temmie is trying to glomp you.", True),
        ("Temmie forgot her other attack.", True),
        ("Temmie is doing her hairs.", True),
        ("Smells like Temmie Flakes.", True),
        ("Temmie vibrates intensely.", True),
        ("Temmiy accidentally misspells her own name.", True),
        ("You flex at Temmie...", True),
        ("Temmie only wants the Temmie Flakes.", True),
        ("You say hello to Temmie.", True)
    )

    @Command.subcommand(hidden=True)
    async def get(self, query=None):
        """hOI!!!!!!"""
        if query is None:
            quote, action = choice(self.QUOTES)
        else:
            quote, action = get_close_matches(
                query, self.QUOTES, n=1, cutoff=0)[0]
        return MessagePacket(quote, action=action)

    DEFAULT = get
