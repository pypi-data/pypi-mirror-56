from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class AbortedTransaction:

    producer_id: int
    first_offset: int

    def __init__(self, producer_id: int, first_offset: int):
        """
        :param producer_id: The producer id associated with the aborted transactions
        :type producer_id: int
        :param first_offset: The first offset in the aborted transaction
        :type first_offset: int
        """
        self.producer_id = producer_id
        self.first_offset = first_offset


class PartitionHeader:

    partition: int
    error_code: ErrorCode
    high_watermark: int
    last_stable_offset: int
    log_start_offset: int
    aborted_transactions: List[AbortedTransaction]
    preferred_read_replica: int

    def __init__(
        self,
        partition: int,
        error_code: ErrorCode,
        high_watermark: int,
        last_stable_offset: int,
        log_start_offset: int,
        aborted_transactions: List[AbortedTransaction],
        preferred_read_replica: int,
    ):
        """
        :param partition: Topic partition id
        :type partition: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param high_watermark: Last committed offset.
        :type high_watermark: int
        :param last_stable_offset: The last stable offset (or LSO) of the partition. This is the last offset such that
                                   the state of all transactional records prior to this offset have been decided
                                   (ABORTED or COMMITTED)
        :type last_stable_offset: int
        :param log_start_offset: Earliest available offset.
        :type log_start_offset: int
        :param aborted_transactions: None
        :type aborted_transactions: List[AbortedTransaction]
        :param preferred_read_replica: The ID of the replica that the consumer should prefer.
        :type preferred_read_replica: int
        """
        self.partition = partition
        self.error_code = error_code
        self.high_watermark = high_watermark
        self.last_stable_offset = last_stable_offset
        self.log_start_offset = log_start_offset
        self.aborted_transactions = aborted_transactions
        self.preferred_read_replica = preferred_read_replica


class PartitionResponse:

    partition_header: PartitionHeader
    record_set: Optional[bytes]

    def __init__(self, partition_header: PartitionHeader, record_set: Optional[bytes]):
        """
        :param partition_header: None
        :type partition_header: PartitionHeader
        :param record_set: None
        :type record_set: Optional[bytes]
        """
        self.partition_header = partition_header
        self.record_set = record_set


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


class FetchResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    session_id: int
    responses: List[Response]
    api_key: ClassVar[ApiKey] = ApiKey.FETCH

    def __init__(self, throttle_time_ms: int, error_code: ErrorCode, session_id: int, responses: List[Response]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param session_id: The fetch session ID
        :type session_id: int
        :param responses: None
        :type responses: List[Response]
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.session_id = session_id
        self.responses = responses
