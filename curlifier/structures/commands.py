import enum
from typing import TypeAlias

CurlCommandShort: TypeAlias = str
CurlCommandLong: TypeAlias = str
CurlCommand: TypeAlias = CurlCommandShort | CurlCommandLong
CurlCommandTitle: TypeAlias = str


class CurlCommandsEnum(enum.Enum):
    """Base class of the command curl structure.

    When initialized, it will take three values: title, short and long.
    """

    def __init__(
        self,
        short: CurlCommandShort,
        long: CurlCommandLong,
        title: CurlCommandTitle,
    ) -> None:
        self._short = short
        self._long = long
        self._title = title

    @property
    def short(self) -> CurlCommandShort:
        """Short form."""
        return self._short

    @property
    def long(self) -> CurlCommandLong:
        """Long form."""
        return self._long

    @property
    def title(self) -> CurlCommandTitle:
        """Human-readable name."""
        return self._title

    def get(self, *, shorted: bool) -> CurlCommand:
        """Returns curl command.

        :param shorted: `True` if you need a short version of the command. Otherwise `False`.
        :type shorted: bool

        :return: Curl command.
        :rtype: CurlCommand
        """
        return self.short if shorted else self.long


@enum.unique
class CommandsConfigureEnum(CurlCommandsEnum):
    """Curl configuration commands."""

    VERBOSE = '-v', '--verbose', 'verbose'
    """Make the operation more talkative."""

    SILENT = '-s', '--silent', 'silent'
    """Silent mode."""

    INSECURE = '-k', '--insecure', 'insecure'
    """Allow insecure server connections."""

    LOCATION = '-L', '--location', 'location'
    """Follow redirects."""

    INCLUDE = '-i', '--include', 'include'
    """Include protocol response headers in the output."""


@enum.unique
class CommandsTransferEnum(CurlCommandsEnum):
    """Curl transfer commands."""

    SEND_DATA = '-d', '--data', 'data'
    """HTTP data (body)."""

    HEADER = '-H', '--header', 'header'
    """Pass custom header(s) to server."""

    REQUEST = '-X', '--request', 'request'
    """Specify request method to use."""

    FORM = '-F', '--form', 'form'
    """Specify multipart MIME data."""
