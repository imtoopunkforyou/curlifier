from typing import Unpack

from requests.models import PreparedRequest, Response

from curlifier.curl import Curl
from curlifier.structures.types import CurlifyRequestConfigure


def curlify(  # noqa: WPS210
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    build_short: bool = False,
    **kwargs: Unpack[CurlifyRequestConfigure],
) -> str:
    location = kwargs.pop('location', False)
    verbose = kwargs.pop('verbose', False)
    silent = kwargs.pop('silent', False)
    insecure = kwargs.pop('insecure', False)
    include = kwargs.pop('include', False)

    curl = Curl(
        response=response,
        prepared_request=prepared_request,
        build_short=build_short,
        location=location,
        verbose=verbose,
        silent=silent,
        insecure=insecure,
        include=include,
    )

    return curl.curlify()
