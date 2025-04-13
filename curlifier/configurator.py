from typing import Self

from curlifier.structures.curl_commands import CurlCommandsConfigureEnum
from curlifier.structures.types import CurlCommand, EmptyStr


class CurlConfig:
    __slots__ = (
        '_location',
        '_verbose',
        '_silent',
        '_insecure',
        '_include',
    )

    def __init__(
        self: Self,
        location: bool,  # True
        verbose: bool,
        silent: bool,
        insecure: bool,
        include: bool,
    ) -> None:
        self._location = location
        self._verbose = verbose
        self._silent = silent
        self._insecure = insecure
        self._include = include


class CurlConfigBuilder(CurlConfig):
    __slots__ = (
        'build_short',
    )

    def __init__(
        self: Self,
        build_short: bool = False,
        **kwargs,
    ) -> None:
        self.build_short = build_short
        super().__init__(**kwargs)

    @property
    def location(self: Self) -> CurlCommand | EmptyStr:
        if self._location:
            command = CurlCommandsConfigureEnum.LOCATION.get_command(shorted=self.build_short)
            return command

        return ''

    @property
    def verbose(self: Self) -> CurlCommand | EmptyStr:
        if self._verbose:
            command = CurlCommandsConfigureEnum.VERBOSE.get_command(shorted=self.build_short)
            return command
        return ''

    @property
    def silent(self: Self) -> CurlCommand | EmptyStr:
        if self._silent:
            command = CurlCommandsConfigureEnum.SILENT.get_command(shorted=self.build_short)
            return command

        return ''

    @property
    def insecure(self: Self) -> CurlCommand | EmptyStr:
        if self._insecure:
            command = CurlCommandsConfigureEnum.INSECURE.get_command(shorted=self.build_short)
            return command

        return ''

    @property
    def include(self: Self) -> CurlCommand | EmptyStr:
        if self._include:
            command = CurlCommandsConfigureEnum.INCLUDE.get_command(shorted=self.build_short)
            return command

        return ''

    def build(self: Self) -> str:
        commands: tuple[CurlCommand | EmptyStr, ...] = (
            self.location,
            self.verbose,
            self.silent,
            self.insecure,
            self.include,
        )

        return ' '.join(commands)
