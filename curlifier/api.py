from typing import Unpack

from requests.models import PreparedRequest, Response

from curlifier.curl import Curl
from curlifier.structures.types import CurlifyConfigure


def curlify(
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    shorted: bool = False,
    **config: Unpack[CurlifyConfigure],
) -> str:
    curl = Curl(
        response=response,
        prepared_request=prepared_request,
        build_short=shorted,
        location=config.pop('location', False),
        verbose=config.pop('verbose', False),
        silent=config.pop('silent', False),
        insecure=config.pop('insecure', False),
        include=config.pop('include', False),
    )

    return curl.curlify()
