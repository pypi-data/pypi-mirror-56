from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

    partition: int
    low_watermark: int
    error_code: ErrorCode

    def __init__(self, partition: int, low_watermark: int, error_code: ErrorCode):
        """
        :param partition: Topic partition id
        :type partition: int
        :param low_watermark: Smallest available offset of all live replicas
        :type low_watermark: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.partition = partition
        self.low_watermark = low_watermark
        self.error_code = error_code


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: None
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class DeleteRecordsResponseData(ResponseData):

    throttle_time_ms: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_RECORDS

    def __init__(self, throttle_time_ms: int, topics: List[Topic]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param topics: None
        :type topics: List[Topic]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topics = topics
