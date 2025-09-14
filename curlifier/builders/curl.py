from typing import ClassVar

from requests.models import PreparedRequest, Response

from curlifier.builders.base import Builder
from curlifier.builders.configurator import ConfigBuilder
from curlifier.builders.transmitter import TransmitterBuilder


class CurlBuilder(Builder):
    """Builds the executable curl command."""

    curl_command: ClassVar[str] = 'curl'

    def __init__(
        self,
        *,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,
        **config: bool,
    ) -> None:
        self._shorted = config.pop('shorted')
        self.config = ConfigBuilder(
            shorted=self._shorted,
            location=config.pop('location'),
            verbose=config.pop('verbose'),
            silent=config.pop('silent'),
            insecure=config.pop('insecure'),
            include=config.pop('include'),
        )
        self.transmitter = TransmitterBuilder(
            response=response,
            prepared_request=prepared_request,
            shorted=self._shorted,
        )

    def build(self) -> str:
        """Collects all parameters into the resulting string.

        If `shorted` is `True` will be collected short version.

        >>> from curlifier.curl import CurlBuilder
        >>> import requests
        >>> r = requests.get('https://example.com/')
        >>> curl_builder = CurlBuilder(
            response=r,
            location=True,
            shorted=True,
            verbose=False,
            silent=False,
            insecure=False,
            include=False,
        )
        >>> curl_builder.build()
        "curl -X GET 'https://example.com/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept: */*' <...> -L"
        """
        built = '{curl_command} {built_transmitter} {built_config}'

        return built.format(
            curl_command=self.curl_command,
            built_transmitter=self.transmitter.build(),
            built_config=self.config.build(),
        )

    @property
    def shorted(self) -> bool:
        """Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._shorted
