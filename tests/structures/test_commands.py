from curlifier.structures.commands import (
    CommandsConfigureEnum,
    CommandsTransferEnum,
)


def test_commands_configure_enum():
    commands_count = 3

    for commands in CommandsConfigureEnum:
        assert commands.get(shorted=True) == commands.short
        assert commands.get(shorted=False) == commands.long
        assert isinstance(commands.value, tuple)
        assert len(commands.value) == commands_count


def test_commands_transfer_enum():
    commands_count = 3

    for commands in CommandsTransferEnum:
        assert commands.get(shorted=True) == commands.short
        assert commands.get(shorted=False) == commands.long
        assert isinstance(commands.value, tuple)
        assert len(commands.value) == commands_count
