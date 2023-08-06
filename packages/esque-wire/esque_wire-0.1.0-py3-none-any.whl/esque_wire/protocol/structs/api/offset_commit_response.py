from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

    partition_index: int
    error_code: ErrorCode

    def __init__(self, partition_index: int, error_code: ErrorCode):
        """
        :param partition_index: The partition index.
        :type partition_index: int
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        """
        self.partition_index = partition_index
        self.error_code = error_code


class Topic:

    name: str
    partitions: List[Partition]

    def __init__(self, name: str, partitions: List[Partition]):
        """
        :param name: The topic name.
        :type name: str
        :param partitions: The responses for each partition in the topic.
        :type partitions: List[Partition]
        """
        self.name = name
        self.partitions = partitions


class OffsetCommitResponseData(ResponseData):

    throttle_time_ms: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_COMMIT

    def __init__(self, throttle_time_ms: int, topics: List[Topic]):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param topics: The responses for each topic.
        :type topics: List[Topic]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topics = topics
