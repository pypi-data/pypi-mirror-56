from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

    error_code: ErrorCode
    partition: int
    leader_epoch: int
    end_offset: int

    def __init__(self, error_code: ErrorCode, partition: int, leader_epoch: int, end_offset: int):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param partition: Topic partition id
        :type partition: int
        :param leader_epoch: The leader epoch
        :type leader_epoch: int
        :param end_offset: The end offset
        :type end_offset: int
        """
        self.error_code = error_code
        self.partition = partition
        self.leader_epoch = leader_epoch
        self.end_offset = end_offset


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: An array of offsets by partition
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class OffsetForLeaderEpochResponseData(ResponseData):

    throttle_time_ms: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_FOR_LEADER_EPOCH

    def __init__(self, throttle_time_ms: int, topics: List[Topic]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param topics: An array of topics for which we have leader offsets for some requested partition leader epoch
        :type topics: List[Topic]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topics = topics
