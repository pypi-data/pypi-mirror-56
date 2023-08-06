from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class PartitionResponse:

    partition: int
    offset: int
    leader_epoch: int
    metadata: Optional[str]
    error_code: ErrorCode

    def __init__(self, partition: int, offset: int, leader_epoch: int, metadata: Optional[str], error_code: ErrorCode):
        """
        :param partition: Topic partition id
        :type partition: int
        :param offset: Message offset to be committed
        :type offset: int
        :param leader_epoch: The leader epoch, if provided is derived from the last consumed record. This is used by
                             the consumer to check for log truncation and to ensure partition metadata is up to date
                             following a group rebalance.
        :type leader_epoch: int
        :param metadata: Any associated metadata the client wants to keep.
        :type metadata: Optional[str]
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.partition = partition
        self.offset = offset
        self.leader_epoch = leader_epoch
        self.metadata = metadata
        self.error_code = error_code


class Response:

    topic: str
    partition_responses: List[PartitionResponse]

    def __init__(self, topic: str, partition_responses: List[PartitionResponse]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_responses: Responses by partition for fetched offsets
        :type partition_responses: List[PartitionResponse]
        """
        self.topic = topic
        self.partition_responses = partition_responses


class OffsetFetchResponseData(ResponseData):

    throttle_time_ms: int
    responses: List[Response]
    error_code: ErrorCode
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_FETCH

    def __init__(self, throttle_time_ms: int, responses: List[Response], error_code: ErrorCode):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param responses: Responses by topic for fetched offsets
        :type responses: List[Response]
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.throttle_time_ms = throttle_time_ms
        self.responses = responses
        self.error_code = error_code
