from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class PartitionError:

    partition: int
    error_code: ErrorCode

    def __init__(self, partition: int, error_code: ErrorCode):
        """
        :param partition: Topic partition id
        :type partition: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.partition = partition
        self.error_code = error_code


class Error:

    topic: str
    partition_errors: List[PartitionError]

    def __init__(self, topic: str, partition_errors: List[PartitionError]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_errors: None
        :type partition_errors: List[PartitionError]
        """
        self.topic = topic
        self.partition_errors = partition_errors


class AddPartitionsToTxnResponseData(ResponseData):

    throttle_time_ms: int
    errors: List[Error]
    api_key: ClassVar[ApiKey] = ApiKey.ADD_PARTITIONS_TO_TXN

    def __init__(self, throttle_time_ms: int, errors: List[Error]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param errors: None
        :type errors: List[Error]
        """
        self.throttle_time_ms = throttle_time_ms
        self.errors = errors
