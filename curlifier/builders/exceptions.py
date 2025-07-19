from requests import PreparedRequest, Response


class DecodeError(TypeError):
    """Data could not be decoded."""

    def __init__(self, decode_data: bytes | str) -> None:
        msg = 'Failed to decode {decode_data}'
        super().__init__(msg.format(decode_data=decode_data))


class MutuallyExclusiveArgsError(ValueError):
    """Raised when mutually exclusive arguments are specified together."""

    def __init__(
        self,
        request: Response | None,
        prepared_request: PreparedRequest | None,
    ) -> None:
        msg = 'Only one argument must be specified: `request={request}` or `prepared_request={prepared_request}`'
        super().__init__(msg.format(request=request, prepared_request=prepared_request))
