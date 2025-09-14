from abc import ABC, abstractmethod


class Builder(ABC):
    """Abstract for builders."""

    __slots__ = ()

    @abstractmethod
    def build(self) -> str:
        """Assembles the result string that is part of the `curl` command."""

    @property
    @abstractmethod
    def shorted(self) -> bool:
        """Specify `True` if you want a short command."""
