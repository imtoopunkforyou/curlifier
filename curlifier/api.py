
from requests.models import PreparedRequest, Response

from curlifier.builders.curl import CurlBuilder, CurlConfig
from curlifier.builders.exceptions import MutuallyExclusiveArgsError


def _validate_input_args(
    response: Response | None,
    prepared_request: PreparedRequest | None,
) -> None:
    """Validate input arguments."""
    if response is None and prepared_request is None:
        error_msg = "Either 'response' or 'prepared_request' must be provided"
        raise ValueError(error_msg)

    if response is not None and prepared_request is not None:
        raise MutuallyExclusiveArgsError(response, prepared_request)


def _validate_config_args(**config: bool) -> None:
    """Validate configuration arguments."""
    valid_config_keys = {'location', 'verbose', 'silent', 'insecure', 'include'}
    invalid_keys = set(config.keys()) - valid_config_keys

    if invalid_keys:
        error_msg = f'Invalid configuration options: {invalid_keys}. Valid options are: {valid_config_keys}'
        raise ValueError(error_msg)

    # Validate that all config values are boolean
    for key, value in config.items():
        if not isinstance(value, bool):
            error_msg = f"Configuration option '{key}' must be a boolean, got {type(value).__name__}"
            raise TypeError(error_msg)


def curlify(
    response: Response | None = None,
    *,
    prepared_request: PreparedRequest | None = None,
    shorted: bool = False,
    **config: bool,
) -> str:
    """The only correct entry point of the `curlifier` library.

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

    :raises ValueError: If invalid arguments are provided.
    :raises TypeError: If configuration values are not boolean.
    :raises MutuallyExclusiveArgsError: If both response and prepared_request are provided.

    >>> import requests
    >>> from curlifier import curlify
    >>> r = requests.get('https://example.com/')
    >>> curlify(r, shorted=True)
    "curl -X GET 'https://example.com/' -H 'User-Agent: python-requests/2.32.3' <...>"
    """
    # Validate input arguments
    _validate_input_args(response, prepared_request)
    _validate_config_args(**config)

    # Validate shorted parameter
    if not isinstance(shorted, bool):
        error_msg = f"Parameter 'shorted' must be a boolean, got {type(shorted).__name__}"
        raise TypeError(error_msg)

    # Create configuration
    curl_config = CurlConfig(
        location=config.get('location', False),
        verbose=config.get('verbose', False),
        silent=config.get('silent', False),
        insecure=config.get('insecure', False),
        include=config.get('include', False),
        build_short=shorted,
    )

    # Build curl command
    curl_builder = CurlBuilder(
        config=curl_config,
        response=response,
        prepared_request=prepared_request,
    )

    return curl_builder.build()
