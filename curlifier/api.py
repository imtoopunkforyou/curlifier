from requests.models import PreparedRequest, Response

from curlifier.curl import Curl


def curlify(  # noqa: WPS211
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    location: bool = False,
    verbose: bool = False,
    silent: bool = False,
    insecure: bool = False,
    include: bool = False,
    build_short: bool = False,
) -> str:
    curl = Curl(
        response=response,
        prepared_request=prepared_request,
        location=location,
        verbose=verbose,
        silent=silent,
        insecure=insecure,
        include=include,
        build_short=build_short,
    )

    return curl.curlify()
