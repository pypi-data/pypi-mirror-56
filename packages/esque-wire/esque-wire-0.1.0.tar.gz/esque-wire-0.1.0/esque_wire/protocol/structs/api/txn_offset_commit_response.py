from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

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


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Responses by partition for committed offsets
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class TxnOffsetCommitResponseData(ResponseData):

    throttle_time_ms: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.TXN_OFFSET_COMMIT

    def __init__(self, throttle_time_ms: int, topics: List[Topic]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param topics: Responses by topic for committed offsets
        :type topics: List[Topic]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topics = topics
