class DecodeError(TypeError):
    """Data could not be decoded."""

    def __init__(self, decode_data: bytes | str) -> None:
        msg = 'Failed to decode {decode_data}'
        super().__init__(msg.format(decode_data=decode_data))


class MutuallyExclusiveArgsError(ValueError):
    """Raised when mutually exclusive arguments are specified together."""

    def __init__(
        self,
        first: str,
        second: str,
    ) -> None:
        msg = 'Only one argument must be specified, but you specified at the same time `{first}` and `{second}`'
        super().__init__(msg.format(first=first, second=second))
