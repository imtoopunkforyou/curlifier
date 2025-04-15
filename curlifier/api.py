from typing import Unpack

from requests.models import PreparedRequest, Response

from curlifier.curl import Curl
from curlifier.structures.types import CurlifyRequestConfigure


def curlify(
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    build_short: bool,
    **kwargs: Unpack[CurlifyRequestConfigure],
) -> str:
    curl = Curl(
        response=response,
        prepared_request=prepared_request,
        build_short=build_short,
        location=kwargs.pop('location', False),
        verbose=kwargs.pop('verbose', False),
        silent=kwargs.pop('silent', False),
        insecure=kwargs.pop('insecure', False),
        include=kwargs.pop('include', False),
    )

    return curl.curlify()
