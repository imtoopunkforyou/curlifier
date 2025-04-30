from typing import ClassVar, Generator, Self, Unpack

from curlifier.builders.base import Builder
from curlifier.structures.commands import CommandsConfigureEnum
from curlifier.structures.types import (
    CurlCommand,
    CurlCommandTitle,
    CurlifyConfigure,
)

type CommandMapping = tuple[tuple[CurlCommandTitle, CommandsConfigureEnum], ...]


class Config:
    """Parameters for curl command configuration."""

    __slots__ = (
        '_location',
        '_verbose',
        '_silent',
        '_insecure',
        '_include',
    )

    command_mapping: ClassVar[CommandMapping] = (
        (CommandsConfigureEnum.LOCATION.title, CommandsConfigureEnum.LOCATION),
        (CommandsConfigureEnum.VERBOSE.title, CommandsConfigureEnum.VERBOSE),
        (CommandsConfigureEnum.SILENT.title, CommandsConfigureEnum.SILENT),
        (CommandsConfigureEnum.INSECURE.title, CommandsConfigureEnum.INSECURE),
        (CommandsConfigureEnum.INCLUDE.title, CommandsConfigureEnum.INCLUDE),
    )
    """Mapping for properties and commands. The property name must match the configuration command title."""

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
        """Follow redirects."""
        return self._location

    @property
    def verbose(self: Self) -> bool:
        """Make the operation more talkative."""
        return self._verbose

    @property
    def silent(self: Self) -> bool:
        """Silent mode."""
        return self._silent

    @property
    def insecure(self: Self) -> bool:
        """Allow insecure server connections."""
        return self._insecure

    @property
    def include(self: Self) -> bool:
        """Include protocol response headers in the output."""
        return self._include


class ConfigBuilder(Config, Builder):
    """Builds a curl command configuration line."""

    __slots__ = (
        '_build_short',
    )

    def __init__(
        self: Self,
        build_short: bool = False,
        **config: Unpack[CurlifyConfigure],
    ) -> None:
        self._build_short = build_short
        super().__init__(**config)

    def build(self: Self) -> str:
        """
        Collects all parameters into the resulting string.

        If `build_short` is `True` will be collected short version.

        >>> from curlifier.configurator import ConfigBuilder
        >>> conf = ConfigBuilder(
            location=True,
            verbose=True,
            silent=False,
            insecure=True,
            include=False,
            build_short=False,
        )
        >>> conf.build()
        '--location --verbose --insecure'
        """
        command_parts = []
        for prop_name, command_enum in self.command_mapping:
            if getattr(self, prop_name):
                command = command_enum.get(shorted=self.build_short)
                command_parts.append(command)

        cleaned_commands: Generator[CurlCommand, None, None] = (
            command for command in command_parts if command
        )

        return ' '.join(cleaned_commands)

    @property
    def build_short(self: Self) -> bool:
        return self._build_short
