from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class PartitionResponse:

    partition: int
    error_code: ErrorCode
    base_offset: int
    log_append_time: int
    log_start_offset: int

    def __init__(
        self, partition: int, error_code: ErrorCode, base_offset: int, log_append_time: int, log_start_offset: int
    ):
        """
        :param partition: Topic partition id
        :type partition: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param base_offset: None
        :type base_offset: int
        :param log_append_time: The timestamp returned by broker after appending the messages. If CreateTime is used
                                for the topic, the timestamp will be -1. If LogAppendTime is used for the topic, the
                                timestamp will be the broker local time when the messages are appended.
        :type log_append_time: int
        :param log_start_offset: The start offset of the log at the time this produce response was created
        :type log_start_offset: int
        """
        self.partition = partition
        self.error_code = error_code
        self.base_offset = base_offset
        self.log_append_time = log_append_time
        self.log_start_offset = log_start_offset


class Response:

    topic: str
    partition_responses: List[PartitionResponse]

    def __init__(self, topic: str, partition_responses: List[PartitionResponse]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_responses: None
        :type partition_responses: List[PartitionResponse]
        """
        self.topic = topic
        self.partition_responses = partition_responses


class ProduceResponseData(ResponseData):

    responses: List[Response]
    throttle_time_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.PRODUCE

    def __init__(self, responses: List[Response], throttle_time_ms: int):
        """
        :param responses: None
        :type responses: List[Response]
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        """
        self.responses = responses
        self.throttle_time_ms = throttle_time_ms
