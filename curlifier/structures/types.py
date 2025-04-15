from typing import Literal

from requests.structures import CaseInsensitiveDict

type HeaderKey = str
type HeaderValue = str
type CurlCommandShort = str
type CurlCommandLong = str
type CurlCommand = CurlCommandShort | CurlCommandLong
type CurlCommandsTuple = tuple[CurlCommandShort, CurlCommandLong]
type HttpMethod = str
type HttpBody = bytes | None
type HttpHeaders = CaseInsensitiveDict
type HttpUrl = str
type FileNameWithExtention = str
type FileFieldName = str
type EmptyStr = Literal['']
type JsonLikeDict = dict[str, str]

# TODO check everything is in use
