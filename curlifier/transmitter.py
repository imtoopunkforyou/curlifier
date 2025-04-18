import copy
import re
from typing import Self

from requests import PreparedRequest, Response

from curlifier.structures.commands import CommandsTransferEnum
from curlifier.structures.http_methods import HttpMethodsEnum
from curlifier.structures.types import (
    EmptyStr,
    FileFieldName,
    FileNameWithExtension,
    HeaderKey,
    PreReqHttpBody,
    PreReqHttpHeaders,
    PreReqHttpMethod,
    PreReqHttpUrl,
)


class PreparedTransmitter:
    """
    Prepares request data for processing.

    Works on a copy of the request object. The original object will not be modified.
    """

    def __init__(
        self: Self,
        response: Response | None = None,
        *,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        if sum(arg is not None for arg in (response, prepared_request)) != 1:
            raise ValueError("Only one argument must be specified: `response` or `prepared_request`")
        self._pre_req: PreparedRequest = (
            prepared_request.copy() if response is None  # type: ignore [union-attr]
            else response.request.copy()
        )

        self._method: PreReqHttpMethod = self._pre_req.method
        self._body: PreReqHttpBody = self._pre_req.body
        self._headers: PreReqHttpHeaders = self._pre_req.headers
        self._url: PreReqHttpUrl = self._pre_req.url

    @property
    def url(self: Self) -> PreReqHttpUrl:
        return self._url

    @property
    def method(self: Self) -> PreReqHttpMethod:
        return self._method

    @property
    def body(self: Self) -> PreReqHttpBody:
        return self._body

    @property
    def headers(self: Self) -> PreReqHttpHeaders:
        cleared_headers = copy.deepcopy(self._headers)
        trash_headers: tuple[HeaderKey] = (
            'Content-Length',
        )
        for header in trash_headers:
            cleared_headers.pop(header, None)

        if 'boundary=' in cleared_headers.get('Content-Type', ''):
            cleared_headers['Content-Type'] = 'multipart/form-data'

        return cleared_headers

    @property
    def has_body(self: Self) -> bool:
        if self._pre_req.method in HttpMethodsEnum.get_methods_with_body():
            return True

        return False


class TransmitterBuilder(PreparedTransmitter):
    """Builds a curl command transfer line."""

    executable_part = '{request_command} {method} \'{url}\' {request_headers} {request_data}'
    executable_request_data = '{command} \'{request_data}\''
    executable_header = '{command} \'{key}: {value}\''
    executable_request_files = '{command} \'{field_name}=@{file_name}\''

    def __init__(
        self: Self,
        build_short: bool,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        self.build_short = build_short
        super().__init__(response, prepared_request=prepared_request)

    def build(self: Self) -> str:
        """
        Collects all parameters into the resulting string.

        If `build_short` is `True` will be collected short version.

        >>> from curlifier.transmitter import TransmitterBuilder
        >>> import requests
        >>> r = requests.get('https://example.com/')
        >>> t = TransmitterBuilder(response=r, build_short=False)
        >>> t.build()
        "--request GET 'https://example.com/' --header 'User-Agent: python-requests/2.32.3' <...>"
        """
        request_command = CommandsTransferEnum.REQUEST.get(shorted=self.build_short)
        request_headers = self._build_executable_headers()
        request_data = self._build_request_data()

        return self.executable_part.format(
            request_command=request_command,
            method=self.method,
            url=self.url,
            request_headers=request_headers,
            request_data=request_data,
        )

    def _build_executable_headers(self: Self) -> str:
        return ' '.join(
            self.executable_header.format(
                command=CommandsTransferEnum.HEADER.get(shorted=self.build_short),
                key=header_key,
                value=header_value,
            ) for header_key, header_value in self.headers.items()
        )

    def _decode_files(self: Self) -> tuple[tuple[FileFieldName, FileNameWithExtension], ...] | None:
        re_expression = rb'name="([^"]+).*?filename="([^"]+)'
        matches = re.findall(
            re_expression,
            self.body,  # type: ignore [arg-type]
            flags=re.DOTALL
        )

        return tuple(
            (
                field_name.decode(),
                file_name.decode(),
            ) for field_name, file_name in matches
        )

    def _decode_raw(self: Self) -> str:
        re_expression = r'\s+'

        return re.sub(re_expression, ' ', str(self.body)).strip()

    def _decode_body(
        self: Self,
    ) -> None | tuple[tuple[FileFieldName, FileNameWithExtension], ...] | str:
        if isinstance(self.body, bytes):
            try:
                return self.body.decode('utf-8')
            except UnicodeDecodeError:
                return self._decode_files()
        elif isinstance(self.body, str):
            return self._decode_raw()

        return None

    def _build_request_data(
        self: Self,
    ) -> str | EmptyStr:
        if self.has_body:
            decode_body = self._decode_body()
            if isinstance(decode_body, str):
                return self.executable_request_data.format(
                    command=CommandsTransferEnum.SEND_DATA.get(shorted=self.build_short),
                    request_data=decode_body,
                )
            elif isinstance(decode_body, tuple):
                executable_files: str = ' '.join(
                    self.executable_request_files.format(
                        command=CommandsTransferEnum.FORM.get(shorted=self.build_short),
                        field_name=field_name,
                        file_name=file_name,
                    ) for field_name, file_name in decode_body
                )
                return executable_files

        return ''
