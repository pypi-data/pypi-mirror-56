from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class PartitionResponse:

    partition: int
    error_code: ErrorCode
    timestamp: int
    offset: int
    leader_epoch: int

    def __init__(self, partition: int, error_code: ErrorCode, timestamp: int, offset: int, leader_epoch: int):
        """
        :param partition: Topic partition id
        :type partition: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param timestamp: The timestamp associated with the returned offset
        :type timestamp: int
        :param offset: The offset found
        :type offset: int
        :param leader_epoch: The leader epoch
        :type leader_epoch: int
        """
        self.partition = partition
        self.error_code = error_code
        self.timestamp = timestamp
        self.offset = offset
        self.leader_epoch = leader_epoch


class Response:

    topic: str
    partition_responses: List[PartitionResponse]

    def __init__(self, topic: str, partition_responses: List[PartitionResponse]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_responses: The listed offsets by partition
        :type partition_responses: List[PartitionResponse]
        """
        self.topic = topic
        self.partition_responses = partition_responses


class ListOffsetsResponseData(ResponseData):

    throttle_time_ms: int
    responses: List[Response]
    api_key: ClassVar[ApiKey] = ApiKey.LIST_OFFSETS

    def __init__(self, throttle_time_ms: int, responses: List[Response]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param responses: The listed offsets by topic
        :type responses: List[Response]
        """
        self.throttle_time_ms = throttle_time_ms
        self.responses = responses
