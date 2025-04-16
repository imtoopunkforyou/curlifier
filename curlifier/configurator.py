from typing import Generator, Self

from curlifier.structures.commands import CommandsConfigureEnum
from curlifier.structures.types import CurlCommand, EmptyStr


class Config:
    __slots__ = (
        '_location',
        '_verbose',
        '_silent',
        '_insecure',
        '_include',
    )

    def __init__(
        self: Self,
        location: bool,
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

    @property
    def location(self: Self) -> bool:
        return self._location

    @property
    def verbose(self: Self) -> bool:
        return self._verbose

    @property
    def silent(self: Self) -> bool:
        return self._silent

    @property
    def insecure(self: Self) -> bool:
        return self._insecure

    @property
    def include(self: Self) -> bool:
        return self._include


class ConfigBuilder(Config):
    __slots__ = (
        'build_short',
    )

    def __init__(
        self: Self,
        build_short: bool = False,
        **kwargs: bool,
    ) -> None:
        self.build_short = build_short
        super().__init__(**kwargs)

    def get_location_command(self: Self) -> CurlCommand | EmptyStr:
        if self.location:
            command = CommandsConfigureEnum.LOCATION.get(shorted=self.build_short)
            return command

        return ''

    def get_verbose_command(self: Self) -> CurlCommand | EmptyStr:
        if self.verbose:
            command = CommandsConfigureEnum.VERBOSE.get(shorted=self.build_short)
            return command
        return ''

    def get_silent_command(self: Self) -> CurlCommand | EmptyStr:
        if self.silent:
            command = CommandsConfigureEnum.SILENT.get(shorted=self.build_short)
            return command

        return ''

    def get_insecure_command(self: Self) -> CurlCommand | EmptyStr:
        if self.insecure:
            command = CommandsConfigureEnum.INSECURE.get(shorted=self.build_short)
            return command

        return ''

    def get_include_command(self: Self) -> CurlCommand | EmptyStr:
        if self.include:
            command = CommandsConfigureEnum.INCLUDE.get(shorted=self.build_short)
            return command

        return ''

    def build(self: Self) -> str:
        commands: tuple[CurlCommand | EmptyStr, ...] = (
            self.get_location_command(),
            self.get_verbose_command(),
            self.get_silent_command(),
            self.get_insecure_command(),
            self.get_include_command(),
        )
        cleaned_commands: Generator[CurlCommand, None, None] = (
            command for command in commands if command
        )

        return ' '.join(cleaned_commands)
