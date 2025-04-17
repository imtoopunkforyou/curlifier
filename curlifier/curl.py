from typing import Self

from requests.models import PreparedRequest, Response

from curlifier.configurator import ConfigBuilder
from curlifier.transmitter import TransmitterBuilder


class CurlBuilder:
    curl_command = 'curl'

    def __init__(  # noqa: WPS211
        self: Self,
        location: bool,
        verbose: bool,
        silent: bool,
        insecure: bool,
        include: bool,
        build_short: bool,
        response: Response | None = None,
        prepared_request: PreparedRequest | None = None,

    ) -> None:
        self.build_short = build_short
        self.config = ConfigBuilder(
            build_short=self.build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        self.transmitter = TransmitterBuilder(
            response=response,
            prepared_request=prepared_request,
            build_short=self.build_short,
        )

    def build(self: Self) -> str:
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
