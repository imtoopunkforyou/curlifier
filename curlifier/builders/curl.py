from typing import ClassVar, TypeVar

from requests.models import PreparedRequest, Response

from curlifier.builders.base import Builder
from curlifier.builders.configurator import ConfigBuilder
from curlifier.builders.transmitter import TransmitterBuilder

SelfCurlBuilder = TypeVar('SelfCurlBuilder', bound='CurlBuilder')


class CurlBuilder(Builder):
    """Builds the executable curl command."""

    curl_command: ClassVar[str] = 'curl'

    def __init__(  # noqa: WPS211
        self: SelfCurlBuilder,
        location: bool,
        verbose: bool,
        silent: bool,
        insecure: bool,
        include: bool,
        build_short: bool,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,

    ) -> None:
        self._build_short = build_short
        self.config = ConfigBuilder(
            build_short=self._build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        self.transmitter = TransmitterBuilder(
            response=response,
            prepared_request=prepared_request,
            build_short=self._build_short,
        )

    def build(self: SelfCurlBuilder) -> str:
        """
        Collects all parameters into the resulting string.

        If `build_short` is `True` will be collected short version.

        >>> from curlifier.curl import CurlBuilder
        >>> import requests
        >>> r = requests.get('https://example.com/')
        >>> curl_builder = CurlBuilder(
            response=r,
            location=True,
            build_short=True,
            verbose=False,
            silent=False,
            insecure=False,
            include=False,
        )
        >>> curl_builder.build()
        "curl -X GET 'https://example.com/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept: */*' <...> -L"
        """
        builded_config: str = self.config.build()
        builded_transmitter: str = self.transmitter.build()
        builded: str = ' '.join(
            (
                self.curl_command,
                builded_transmitter,
                builded_config,
            ),
        )

        return builded

    @property
    def build_short(self: SelfCurlBuilder) -> bool:
        """
        Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._build_short
