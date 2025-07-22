from dataclasses import dataclass
from typing import ClassVar

from requests.models import PreparedRequest, Response

from curlifier.builders.base import Builder
from curlifier.builders.configurator import ConfigBuilder
from curlifier.builders.transmitter import TransmitterBuilder


@dataclass
class CurlConfig:
    """Configuration options for curl command generation."""

    location: bool = False
    verbose: bool = False
    silent: bool = False
    insecure: bool = False
    include: bool = False
    build_short: bool = False

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        # Ensure silent and verbose are not both True
        if self.silent and self.verbose:
            error_msg = "Cannot use both 'silent' and 'verbose' options simultaneously"
            raise ValueError(error_msg)


class CurlBuilder(Builder):
    """Builds the executable curl command."""

    curl_command: ClassVar[str] = 'curl'

    def __init__(
        self,
        *,
        config: CurlConfig,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,
    ) -> None:
        self._config = config
        self.config_builder = ConfigBuilder(
            build_short=self._config.build_short,
            location=self._config.location,
            verbose=self._config.verbose,
            silent=self._config.silent,
            insecure=self._config.insecure,
            include=self._config.include,
        )
        self.transmitter = TransmitterBuilder(
            response=response,
            prepared_request=prepared_request,
            build_short=self._config.build_short,
        )

    def build(self) -> str:
        """Collects all parameters into the resulting string.

        If `build_short` is `True` will be collected short version.

        >>> from curlifier.builders.curl import CurlBuilder, CurlConfig
        >>> import requests
        >>> r = requests.get('https://example.com/')
        >>> config = CurlConfig(location=True, build_short=True)
        >>> curl_builder = CurlBuilder(config=config, response=r)
        >>> curl_builder.build()
        "curl -X GET 'https://example.com/' -H 'Accept-Encoding: gzip, deflate' -H 'Accept: */*' <...> -L"
        """
        built_command = '{curl_command} {built_transmitter} {built_config}'

        return built_command.format(
            curl_command=self.curl_command,
            built_transmitter=self.transmitter.build(),
            built_config=self.config_builder.build(),
        )

    @property
    def build_short(self) -> bool:
        """Controlling the form of command.

        :return: `True` and command will be short. Otherwise `False`.
        :rtype: bool
        """
        return self._config.build_short
