import enum
from typing import Self

from curlifier.structures.types import (
    CurlCommand,
    CurlCommandLong,
    CurlCommandShort,
)


class CommandsEnum(enum.Enum):
    """
    Base class of the command curl structure.
    When initialized, it will take two values: short and long.
    """

    def __init__(self: Self, short: CurlCommandShort, long: CurlCommandLong) -> None:
        self.short = short
        self.long = long

    def get(self: Self, *, shorted: bool) -> CurlCommand:
        """
        Returns curl command.

        :param shorted: `True` if you need a short version of the command. Otherwise `False`.
        :type shorted: bool

        :return: Curl command.
        :rtype: CurlCommand
        """
        return self.short if shorted else self.long

    def __str__(self: Self) -> CurlCommandLong:
        return self.long


@enum.unique
class CommandsConfigureEnum(CommandsEnum):
    """Curl configuration commands."""

    VERBOSE = ('-v', '--verbose')
    """Make the operation more talkative."""

    SILENT = ('-s', '--silent')
    """Silent mode."""

    INSECURE = ('-k', '--insecure')
    """Allow insecure server connections."""

    LOCATION = ('-L', '--location')
    """Follow redirects."""

    INCLUDE = ('-i', '--include')
    """Include protocol response headers in the output."""


@enum.unique
class CommandsTransferEnum(CommandsEnum):
    """Curl transfer commands."""

    SEND_DATA = ('-d', '--data')
    """HTTP data (body)."""

    HEADER = ('-H', '--header')
    """Pass custom header(s) to server."""

    REQUEST = ('-X', '--request')
    """Specify request method to use."""

    FORM = ('-F', '--form')
    """Specify multipart MIME data."""
