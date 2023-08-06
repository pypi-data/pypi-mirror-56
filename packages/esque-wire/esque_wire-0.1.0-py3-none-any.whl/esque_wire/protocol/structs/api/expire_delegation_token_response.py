from typing import ClassVar

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class ExpireDelegationTokenResponseData(ResponseData):

    error_code: ErrorCode
    expiry_timestamp: int
    throttle_time_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.EXPIRE_DELEGATION_TOKEN

    def __init__(self, error_code: ErrorCode, expiry_timestamp: int, throttle_time_ms: int):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param expiry_timestamp: timestamp (in msec) at which this token expires..
        :type expiry_timestamp: int
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        """
        self.error_code = error_code
        self.expiry_timestamp = expiry_timestamp
        self.throttle_time_ms = throttle_time_ms
