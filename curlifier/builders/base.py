from abc import ABC, abstractmethod
from typing import Self


class Builder(ABC):
    """Abstract for builders."""
    @abstractmethod
    def build(self: Self) -> str:
        """Assembles the result string that is part of the `curl` command."""
