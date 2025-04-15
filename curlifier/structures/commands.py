import enum
from typing import Self

from curlifier.structures.types import (
    CurlCommand,
    CurlCommandLong,
    CurlCommandShort,
)


class CommandsEnum(enum.Enum):
    def __init__(self: Self, short: CurlCommandShort, long: CurlCommandLong) -> None:
        self.short = short
        self.long = long

    def get(self: Self, *, shorted: bool) -> CurlCommand:
        return self.short if shorted else self.long

    def __str__(self: Self) -> CurlCommandLong:
        return self.long


@enum.unique
class CommandsConfigureEnum(CommandsEnum):
    VERBOSE = ('-v', '--verbose')
    SILENT = ('-s', '--silent')
    INSECURE = ('-k', '--insecure')
    LOCATION = ('-L', '--location')
    INCLUDE = ('-i', '--include')


@enum.unique
class CommandsTransferEnum(CommandsEnum):
    SEND_DATA = ('-d', '--data')
    HEADER = ('-H', '--header')
    REQUEST = ('-X', '--request')
    FORM = ('-F', '--form')
