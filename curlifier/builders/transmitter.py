import copy
import re
from typing import Any, ClassVar, Literal, TypeAlias

from requests import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

from curlifier.builders.base import Builder
from curlifier.builders.exceptions import DecodeError, MutuallyExclusiveArgsError
from curlifier.structures.commands import CommandsTransferEnum
from curlifier.structures.http_methods import HttpMethodsEnum

ExecutableTemplate: TypeAlias = str
EmptyStr: TypeAlias = Literal['']
HeaderKey: TypeAlias = str
PreReqHttpMethod: TypeAlias = str | Any | None
PreReqHttpBody: TypeAlias = bytes | str | Any | None
PreReqHttpHeaders: TypeAlias = CaseInsensitiveDict[str]
PreReqHttpUrl: TypeAlias = str | Any | None
FileNameWithExtension: TypeAlias = str
FileFieldName: TypeAlias = str


class Decoder:
    """Decodes the raw body of the request."""

    __slots__ = ()

    def decode(
        self,
        data_for_decode: bytes | str,
    ) -> tuple[tuple[FileFieldName, FileNameWithExtension], ...] | str:
        """Decodes request bodies of different types: json, raw-data or files.

        :param data_for_decode: Request body.
        :type data_for_decode: bytes | str

        :raises TypeError: In case the body could not be decoded.

        :return: Decoded obj.
        :rtype: tuple[tuple[FileFieldName, FileNameWithExtension], ...] | str
        """
        if isinstance(data_for_decode, bytes):
            try:
                return data_for_decode.decode('utf-8')
            except UnicodeDecodeError:
                return self._decode_files(data_for_decode)
        elif isinstance(data_for_decode, str):
            return self._decode_raw(data_for_decode)

        raise DecodeError(data_for_decode)

    def _decode_raw(
        self,
        data_for_decode: str,
    ) -> str:
        re_expression = r'\s+'

        return re.sub(re_expression, ' ', str(data_for_decode)).strip()

    def _decode_files(
        self,
        data_for_decode: bytes,
    ) -> tuple[tuple[FileFieldName, FileNameWithExtension], ...]:
        re_expression = rb'name="([^"]+).*?filename="([^"]+)'
        matches = re.findall(
            re_expression,
            data_for_decode,
            flags=re.DOTALL,
        )

        return tuple(
            (
                field_name.decode(),
                file_name.decode(),
            )
            for field_name, file_name in matches
        )


class PreparedTransmitter:
    """Prepares request data for processing.

    Works on a copy of the request object.
    The original object will not be modified.
    """

    __slots__ = (
        '_body',
        '_headers',
        '_method',
        '_pre_req',
        '_response',
        '_url',
    )

    def __init__(
        self,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        if sum(arg is not None for arg in (response, prepared_request)) != 1:
            raise MutuallyExclusiveArgsError(response, prepared_request)

        self._response = response
        self._pre_req: PreparedRequest = (
            prepared_request.copy()  # type: ignore [union-attr]
            if self._response is None
            else self._response.request.copy()
        )

        self._method: PreReqHttpMethod = self._pre_req.method
        self._body: PreReqHttpBody = self._pre_req.body
        self._headers: PreReqHttpHeaders = self._pre_req.headers
        self._url: PreReqHttpUrl = self._pre_req.url

    @property
    def url(self) -> PreReqHttpUrl:
        """Url from `Response` or `PreparedRequest` object."""
        return self._url

    @property
    def method(self) -> PreReqHttpMethod:
        """Method from `Response` or `PreparedRequest` object."""
        return self._method

    @property
    def body(self) -> PreReqHttpBody:
        """Body from `Response` or `PreparedRequest` object."""
        return self._body

    @property
    def headers(self) -> PreReqHttpHeaders:
        """Headers from `Response` or `PreparedRequest` object."""
        cleared_headers = copy.deepcopy(self._headers)
        trash_headers: tuple[HeaderKey] = ('Content-Length',)
        for header in trash_headers:
            cleared_headers.pop(header, None)

        if 'boundary=' in cleared_headers.get('Content-Type', ''):
            cleared_headers['Content-Type'] = 'multipart/form-data'

        return cleared_headers

    @property
    def has_body(self) -> bool:
        """True if there is a request body."""
        return bool(self._pre_req.method in HttpMethodsEnum.get_methods_with_body())


class TransmitterBuilder(PreparedTransmitter, Decoder, Builder):
    """Builds a curl command transfer part."""

    __slots__ = ('_shorted',)

    built: ClassVar[ExecutableTemplate] = "{request_command} {method} '{url}' {request_headers} {request_data}"
    """The template of the resulting executable command."""

    request_data: ClassVar[ExecutableTemplate] = "{command} '{request_data}'"
    """Resulting collected data template."""

    header: ClassVar[ExecutableTemplate] = "{command} '{key}: {value}'"
    """Resulting collected header template."""

    request_file: ClassVar[ExecutableTemplate] = "{command} '{field_name}=@{file_name}'"
    """Resulting collected file template."""

    def __init__(
        self,
        response: Response | None = None,
        *,
        shorted: bool,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        self._shorted = shorted
        super().__init__(response, prepared_request=prepared_request)

    def build(self) -> str:
        """Collects all parameters into the resulting string.

        If `shorted` is `True` will be collected short version.

        >>> from curlifier.transmitter import TransmitterBuilder
        >>> import requests
        >>> r = requests.get('https://example.com/')
        >>> t = TransmitterBuilder(response=r, shorted=False)
        >>> t.build()
        "--request GET 'https://example.com/' --header 'User-Agent: python-requests/2.32.3' <...>"
        """
        request_command = CommandsTransferEnum.REQUEST.get(shorted=self._shorted)
        request_headers = self._build_executable_headers()
        request_data = self._build_executable_data()

        return self.built.format(
            request_command=request_command,
            method=self.method,
            url=self.url,
            request_headers=request_headers,
            request_data=request_data,
        )

    @property
    def shorted(self) -> bool:
        """Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._shorted

    def _build_executable_headers(self) -> str:
        return ' '.join(
            self.header.format(
                command=CommandsTransferEnum.HEADER.get(shorted=self._shorted),
                key=header_key,
                value=header_value,
            )
            for header_key, header_value in self.headers.items()
        )

    def _build_executable_data(
        self,
    ) -> str | EmptyStr:
        if self.has_body:
            decode_body = self.decode(self.body)  # type: ignore [arg-type]
            if isinstance(decode_body, str):
                return self.request_data.format(
                    command=CommandsTransferEnum.SEND_DATA.get(shorted=self._shorted),
                    request_data=decode_body,
                )
            if isinstance(decode_body, tuple):
                executable_files: str = ' '.join(
                    self.request_file.format(
                        command=CommandsTransferEnum.FORM.get(shorted=self._shorted),
                        field_name=field_name,
                        file_name=file_name,
                    )
                    for field_name, file_name in decode_body
                )
                return executable_files

        return ''
