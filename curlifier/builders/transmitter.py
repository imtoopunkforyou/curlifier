import copy
import re
from typing import Any, ClassVar, Literal, TypeAlias, TypeVar

from requests import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

from curlifier.builders.base import Builder
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

SelfDecoder = TypeVar('SelfDecoder', bound='Decoder')
SelfPreparedTransmitter = TypeVar('SelfPreparedTransmitter', bound='PreparedTransmitter')
SelfTransmitterBuilder = TypeVar('SelfTransmitterBuilder', bound='TransmitterBuilder')


class Decoder:
    """Decodes the raw body of the request."""
    def decode(
        self: SelfDecoder,
        data_for_decode: bytes | str,
    ) -> None | tuple[tuple[FileFieldName, FileNameWithExtension], ...] | str:
        """
        Decodes request bodies of different types: json, raw-data or files.

        :param data_for_decode: Request body.
        :type data_for_decode: bytes | str

        :return: Decoded obj.
        :rtype: None | tuple[tuple[FileFieldName, FileNameWithExtension], ...] | str
        """
        if isinstance(data_for_decode, bytes):
            try:
                return data_for_decode.decode('utf-8')
            except UnicodeDecodeError:
                return self._decode_files(data_for_decode)
        elif isinstance(data_for_decode, str):
            return self._decode_raw(data_for_decode)

        return None

    def _decode_raw(
        self: SelfDecoder,
        data_for_decode: str,
    ) -> str:
        re_expression = r'\s+'

        return re.sub(re_expression, ' ', str(data_for_decode)).strip()

    def _decode_files(
        self: SelfDecoder,
        data_for_decode: bytes,
    ) -> tuple[tuple[FileFieldName, FileNameWithExtension], ...] | None:
        re_expression = rb'name="([^"]+).*?filename="([^"]+)'
        matches = re.findall(
            re_expression,
            data_for_decode,
            flags=re.DOTALL
        )

        return tuple(
            (
                field_name.decode(),
                file_name.decode(),
            ) for field_name, file_name in matches
        )


class PreparedTransmitter:
    """
    Prepares request data for processing.

    Works on a copy of the request object. The original object will not be modified.
    """

    def __init__(
        self: SelfPreparedTransmitter,
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
    def url(self: SelfPreparedTransmitter) -> PreReqHttpUrl:
        return self._url

    @property
    def method(self: SelfPreparedTransmitter) -> PreReqHttpMethod:
        return self._method

    @property
    def body(self: SelfPreparedTransmitter) -> PreReqHttpBody:
        return self._body

    @property
    def headers(self: SelfPreparedTransmitter) -> PreReqHttpHeaders:
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
    def has_body(self: SelfPreparedTransmitter) -> bool:
        if self._pre_req.method in HttpMethodsEnum.get_methods_with_body():
            return True

        return False


class TransmitterBuilder(PreparedTransmitter, Decoder, Builder):
    """Builds a curl command transfer part."""

    builded: ClassVar[ExecutableTemplate] = '{request_command} {method} \'{url}\' {request_headers} {request_data}'
    """The template of the resulting executable command."""

    request_data: ClassVar[ExecutableTemplate] = '{command} \'{request_data}\''
    """Resulting collected data template."""

    header: ClassVar[ExecutableTemplate] = '{command} \'{key}: {value}\''
    """Resulting collected header template."""

    request_file: ClassVar[ExecutableTemplate] = '{command} \'{field_name}=@{file_name}\''
    """Resulting collected file template."""

    def __init__(
        self: SelfTransmitterBuilder,
        build_short: bool,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        self._build_short = build_short
        super().__init__(response, prepared_request=prepared_request)

    def build(self: SelfTransmitterBuilder) -> str:
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
        request_data = self._build_executable_data()

        return self.builded.format(
            request_command=request_command,
            method=self.method,
            url=self.url,
            request_headers=request_headers,
            request_data=request_data,
        )

    @property
    def build_short(self: SelfTransmitterBuilder) -> bool:
        """
        Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._build_short

    def _build_executable_headers(self: SelfTransmitterBuilder) -> str:
        return ' '.join(
            self.header.format(
                command=CommandsTransferEnum.HEADER.get(shorted=self.build_short),
                key=header_key,
                value=header_value,
            ) for header_key, header_value in self.headers.items()
        )

    def _build_executable_data(
        self: SelfTransmitterBuilder,
    ) -> str | EmptyStr:
        if self.has_body:
            decode_body = self.decode(self.body)  # type: ignore [arg-type]
            if isinstance(decode_body, str):
                return self.request_data.format(
                    command=CommandsTransferEnum.SEND_DATA.get(shorted=self.build_short),
                    request_data=decode_body,
                )
            elif isinstance(decode_body, tuple):
                executable_files: str = ' '.join(
                    self.request_file.format(
                        command=CommandsTransferEnum.FORM.get(shorted=self.build_short),
                        field_name=field_name,
                        file_name=file_name,
                    ) for field_name, file_name in decode_body
                )
                return executable_files

        return ''
