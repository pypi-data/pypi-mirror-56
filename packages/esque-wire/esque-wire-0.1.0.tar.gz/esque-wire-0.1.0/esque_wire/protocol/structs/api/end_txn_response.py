from typing import ClassVar

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class EndTxnResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    api_key: ClassVar[ApiKey] = ApiKey.END_TXN

    def __init__(self, throttle_time_ms: int, error_code: ErrorCode):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
