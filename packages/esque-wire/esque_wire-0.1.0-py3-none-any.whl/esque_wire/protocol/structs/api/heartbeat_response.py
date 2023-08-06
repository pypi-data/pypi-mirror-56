from typing import ClassVar

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class HeartbeatResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    api_key: ClassVar[ApiKey] = ApiKey.HEARTBEAT

    def __init__(self, throttle_time_ms: int, error_code: ErrorCode):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
