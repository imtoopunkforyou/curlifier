from abc import ABC, abstractmethod
from typing import TypeVar

SelfBuilder = TypeVar('SelfBuilder', bound='Builder')


class Builder(ABC):
    """Abstract for builders."""

    @abstractmethod
    def build(self: SelfBuilder) -> str:
        """Assembles the result string that is part of the `curl` command."""
        ...

    @property
    @abstractmethod
    def build_short(self: SelfBuilder) -> bool:
        """Specify `True` if you want a short command."""
        ...
