from typing import Any, Literal, TypedDict

from requests.structures import CaseInsensitiveDict


class CurlifyConfigure(TypedDict, total=False):
    location: bool
    verbose: bool
    silent: bool
    insecure: bool
    include: bool


type HeaderKey = str
type HeaderValue = str
type CurlCommandShort = str
type CurlCommandLong = str
type CurlCommand = CurlCommandShort | CurlCommandLong
type HttpMethod = str
type PreReqHttpMethod = str | Any | None
type PreReqHttpBody = bytes | str | Any | None
type PreReqHttpHeaders = CaseInsensitiveDict
type PreReqHttpUrl = str | Any | None
type FileNameWithExtension = str
type FileFieldName = str
type EmptyStr = Literal['']
