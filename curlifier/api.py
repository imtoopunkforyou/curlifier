from requests.models import PreparedRequest, Response

from curlifier.builders.curl import CurlBuilder


def curlify(
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    shorted: bool = False,
    **config: bool,
) -> str:
    """
    The only correct entry point of the `curlifier` library.

    :param response: The `requests` library Response object.
                     Must be specified if the `prepared_request` argument is not specified.
    :type response: Response | None, optional

    :param prepared_request: The `requests` library `PreparedRequest` object.
                             Must be specified if the `response` argument is not specified.
    :type prepared_request: PreparedRequest | None, optional

    :param shorted: Specify `True` if you want to build the curl command in a shortened form.
                    Otherwise `False`. Defaults to `False`.
    :type shorted: bool

    :param config: Additional configuration options for curl command:
        - location (bool) - Follow redirects. Defaults to `False`.
        - verbose (bool) - Verbose output. Defaults to `False`.
        - silent (bool) - Silent mode. Defaults to `False`.
        - insecure (bool) - Allow insecure connections. Defaults to `False`.
        - include (bool) - Include protocol headers. Defaults to `False`.
    :type config: bool

    :return: Executable curl command.
    :rtype: str

    >>> import requests
    >>> from curlifier import curlify
    >>> r = requests.get('https://example.com/')
    >>> curlify(r, shorted=True)
    "curl -X GET 'https://example.com/' -H 'User-Agent: python-requests/2.32.3' <...>"
    """
    curl_builder = CurlBuilder(
        response=response,
        prepared_request=prepared_request,
        build_short=shorted,
        location=config.pop('location', False),
        verbose=config.pop('verbose', False),
        silent=config.pop('silent', False),
        insecure=config.pop('insecure', False),
        include=config.pop('include', False),
    )
    curl: str = curl_builder.build()

    return curl
