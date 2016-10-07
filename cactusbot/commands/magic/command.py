"""Manage commands."""


from . import Command
from ...packets import MessagePacket


class Meta(Command):
    """Manage commands."""

    COMMAND = "command"

    permissions = {
        '+': "Mod",
        '$': "Subscriber"
    }

    @Command.subcommand
    async def add(self, name: r'!?([+$]?)(.+)', *response,
                  added_by: "username"):
        """Add a command."""

        permissions = ','.join(self.permissions[symbol] for symbol in name[0])

        data = await self.api.add_command(
            name[1], ' '.join(response), permissions=permissions,
            added_by=added_by
        )
        if data[0].get("meta")["updated"]:
            return MessagePacket(
                ("text", "Updated command !{}.".format(name[1])),
                user="BOT USER"
            )
        elif data[0].get("meta")["created"]:
            return MessagePacket(
                ("text", "Added command !{}.".format(name[1])),
                user="BOT USER"
            )

    @Command.subcommand
    async def remove(self, name: "?command", *, removed_by: "username"):
        """Remove a command."""
        removed = await self.api.remove_command(name, removed_by=removed_by)
        if removed:
            return MessagePacket(
                ("text", "Removed command !{}.".format(name)),
                user="BOT USER"
            )
        return MessagePacket(
            ("text", "Command !{} does not exist!".format(name)),
            user="BOT USER"
        )

    @Command.subcommand
    async def list(self):
        """List all custom commands."""
        commands = await self.api.get_command()

        if commands:
            return MessagePacket(
                ("text",
                 "Commands: {}".format(', '.join(
                     command["data"]["attributes"]["name"] for
                     command in commands
                     ))
                 ),
                user="BOT USER"
            )
        return MessagePacket(
            ("text", "No commands added!"),
            user="BOT USER"
        )
