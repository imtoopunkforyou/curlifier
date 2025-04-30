from typing import TypedDict


class CurlifyConfigure(TypedDict, total=False):
    location: bool
    verbose: bool
    silent: bool
    insecure: bool
    include: bool


type CurlCommandShort = str
type CurlCommandLong = str
type CurlCommand = CurlCommandShort | CurlCommandLong
type CurlCommandTitle = str
