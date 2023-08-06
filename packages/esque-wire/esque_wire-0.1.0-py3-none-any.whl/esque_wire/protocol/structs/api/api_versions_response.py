from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class ApiVersion:

    api_key: ApiKey
    min_version: int
    max_version: int

    def __init__(self, api_key: ApiKey, min_version: int, max_version: int):
        """
        :param api_key: API key.
        :type api_key: ApiKey
        :param min_version: Minimum supported version.
        :type min_version: int
        :param max_version: Maximum supported version.
        :type max_version: int
        """
        self.api_key = api_key
        self.min_version = min_version
        self.max_version = max_version


class ApiVersionsResponseData(ResponseData):

    error_code: ErrorCode
    api_versions: List[ApiVersion]
    throttle_time_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.API_VERSIONS

    def __init__(self, error_code: ErrorCode, api_versions: List[ApiVersion], throttle_time_ms: int):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param api_versions: API versions supported by the broker.
        :type api_versions: List[ApiVersion]
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        """
        self.error_code = error_code
        self.api_versions = api_versions
        self.throttle_time_ms = throttle_time_ms
