from typing import ClassVar

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class InitProducerIdResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    producer_id: int
    producer_epoch: int
    api_key: ClassVar[ApiKey] = ApiKey.INIT_PRODUCER_ID

    def __init__(self, throttle_time_ms: int, error_code: ErrorCode, producer_id: int, producer_epoch: int):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param producer_id: The current producer id.
        :type producer_id: int
        :param producer_epoch: The current epoch associated with the producer id.
        :type producer_epoch: int
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
