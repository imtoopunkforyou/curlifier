from curlifier.structures.commands import (
    CommandsConfigureEnum,
    CommandsTransferEnum,
)


def test_commands_configure_enum():
    for commands in CommandsConfigureEnum:
        assert commands.get(shorted=True) == commands.short
        assert commands.get(shorted=False) == commands.long
        assert str(commands) == commands.long
        assert isinstance(commands.value, tuple)


def test_commands_transfer_enum():
    for commands in CommandsTransferEnum:
        assert commands.get(shorted=True) == commands.short
        assert commands.get(shorted=False) == commands.long
        assert str(commands) == commands.long
        assert isinstance(commands.value, tuple)
