import enum
from typing import TypeAlias

HttpMethod: TypeAlias = str


@enum.unique
class HttpMethodsEnum(enum.Enum):
    """Supported HTTP methods."""

    GET = 'GET'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

    @classmethod
    def get_methods_without_body(cls: type['HttpMethodsEnum']) -> tuple[HttpMethod, HttpMethod, HttpMethod, HttpMethod]:
        """HTTP methods methods that have a body in the structure."""
        return (
            cls.GET.value,
            cls.HEAD.value,
            cls.DELETE.value,
            cls.OPTIONS.value,
        )

    @classmethod
    def get_methods_with_body(cls: type['HttpMethodsEnum']) -> tuple[HttpMethod, HttpMethod, HttpMethod]:
        """HTTP methods that do not have a body in the structure"""
        return (
            cls.POST.value,
            cls.PUT.value,
            cls.PATCH.value,
        )
