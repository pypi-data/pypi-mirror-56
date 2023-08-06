from typing import ClassVar

from ..constants import ApiKey


class RequestData:
    api_key: ClassVar[ApiKey]


class ResponseData:
    api_key: ClassVar[ApiKey]
