import enum
from typing import Self

from curlifier.structures.types import HttpMethod


@enum.unique
class HttpMethodsEnum(enum.Enum):
    GET: HttpMethod = 'GET'
    OPTIONS: HttpMethod = 'OPTIONS'
    HEAD: HttpMethod = 'HEAD'
    POST: HttpMethod = 'POST'
    PUT: HttpMethod = 'PUT'
    PATCH: HttpMethod = 'PATCH'
    DELETE: HttpMethod = 'DELETE'

    @classmethod
    def get_methods_without_body(cls: type[Self]) -> tuple[HttpMethod, HttpMethod, HttpMethod, HttpMethod]:
        return (
            cls.GET.value,
            cls.HEAD.value,
            cls.DELETE.value,
            cls.OPTIONS.value,
        )

    @classmethod
    def get_methods_with_body(cls: type[Self]) -> tuple[HttpMethod, HttpMethod, HttpMethod]:
        return (
            cls.POST.value,
            cls.PUT.value,
            cls.PATCH.value,
        )
