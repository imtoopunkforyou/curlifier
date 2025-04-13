import enum
from typing import Self

from curlifier.structures.types import (
    CurlCommand,
    CurlCommandLong,
    CurlCommandShort,
    CurlCommandsTuple,
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
class CommandsConfigureEnum(CommandsEnum):  # TODO off lint
    VERBOSE: CurlCommandsTuple = ('-v', '--verbose')
    SILENT: CurlCommandsTuple = ('-s', '--silent')
    INSECURE: CurlCommandsTuple = ('-k', '--insecure')
    LOCATION: CurlCommandsTuple = ('-L', '--location')
    INCLUDE: CurlCommandsTuple = ('-i', '--include')


@enum.unique
class CommandsTransferEnum(CommandsEnum):
    SEND_DATA: CurlCommandsTuple = ('-d', '--data')
    HEADER: CurlCommandsTuple = ('-H', '--header')
    REQUEST: CurlCommandsTuple = ('-X', '--request')
    FORM: CurlCommandsTuple = ('-F', '--form')
