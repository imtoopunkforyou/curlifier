from typing import TYPE_CHECKING, ClassVar, TypeAlias

from curlifier.builders.base import Builder
from curlifier.structures.commands import (
    CommandsConfigureEnum,
    CurlCommand,
    CurlCommandTitle,
)

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Generator

CommandMapping: TypeAlias = tuple[tuple[CurlCommandTitle, CommandsConfigureEnum], ...]


class Config:
    """Parameters for curl command configuration."""

    __slots__ = (
        '_include',
        '_insecure',
        '_location',
        '_silent',
        '_verbose',
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
        self,
        *,
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
    def location(self) -> bool:
        """Follow redirects."""
        return self._location

    @property
    def verbose(self) -> bool:
        """Make the operation more talkative."""
        return self._verbose

    @property
    def silent(self) -> bool:
        """Silent mode."""
        return self._silent

    @property
    def insecure(self) -> bool:
        """Allow insecure server connections."""
        return self._insecure

    @property
    def include(self) -> bool:
        """Include protocol response headers in the output."""
        return self._include


class ConfigBuilder(Config, Builder):
    """Builds a curl command configuration line."""

    __slots__ = ('_shorted',)

    def __init__(
        self,
        *,
        shorted: bool,
        **config: bool,
    ) -> None:
        self._shorted = shorted
        super().__init__(**config)

    def build(self) -> str:
        """Collects all parameters into the resulting string.

        If `shorted` is `True` will be collected short version.

        >>> from curlifier.configurator import ConfigBuilder
        >>> conf = ConfigBuilder(
            location=True,
            verbose=True,
            silent=False,
            insecure=True,
            include=False,
            shorted=False,
        )
        >>> conf.build()
        '--location --verbose --insecure'
        """
        command_parts = []
        for prop_name, command_enum in self.command_mapping:
            if getattr(self, prop_name):
                command = command_enum.get(shorted=self.shorted)
                command_parts.append(command)

        cleaned_commands: Generator[CurlCommand, None, None] = (command for command in command_parts if command)

        return ' '.join(cleaned_commands)

    @property
    def shorted(self) -> bool:
        """Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._shorted
