import enum
from typing import Self

from curlifier.structures.types import (
    CurlCommand,
    CurlCommandLong,
    CurlCommandShort,
    CurlCommandTitle,
)


class CommandsEnum(enum.Enum):
    """
    Base class of the command curl structure.
    When initialized, it will take three values: title, short and long.
    """
    __slots__ = (
        '_short',
        '_long',
        '_title',
    )

    def __init__(
        self: Self,
        short: CurlCommandShort,
        long: CurlCommandLong,
        title: CurlCommandTitle,
    ) -> None:
        self._short = short
        self._long = long
        self._title = title

    @property
    def short(self: Self) -> str:
        """Short form."""
        return self._short

    @property
    def long(self: Self) -> str:
        """Long form."""
        return self._long

    @property
    def title(self: Self) -> str:
        """Human-readble name."""
        return self._title

    def get(self: Self, *, shorted: bool) -> CurlCommand:
        """
        Returns curl command.

        :param shorted: `True` if you need a short version of the command. Otherwise `False`.
        :type shorted: bool

        :return: Curl command.
        :rtype: CurlCommand
        """
        return self.short if shorted else self.long

    def __str__(self: Self) -> CurlCommandTitle:
        return self.title


@enum.unique
class CommandsConfigureEnum(CommandsEnum):
    """Curl configuration commands."""

    VERBOSE = ('-v', '--verbose', 'verbose')
    """Make the operation more talkative."""

    SILENT = ('-s', '--silent', 'silent')
    """Silent mode."""

    INSECURE = ('-k', '--insecure', 'insecure')
    """Allow insecure server connections."""

    LOCATION = ('-L', '--location', 'location')
    """Follow redirects."""

    INCLUDE = ('-i', '--include', 'include')
    """Include protocol response headers in the output."""


@enum.unique
class CommandsTransferEnum(CommandsEnum):
    """Curl transfer commands."""

    SEND_DATA = ('-d', '--data', 'data')
    """HTTP data (body)."""

    HEADER = ('-H', '--header', 'header')
    """Pass custom header(s) to server."""

    REQUEST = ('-X', '--request', 'request')
    """Specify request method to use."""

    FORM = ('-F', '--form', 'form')
    """Specify multipart MIME data."""
