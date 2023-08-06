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
        :param partitions: None
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class TransactionMarker:

    producer_id: int
    topics: List[Topic]

    def __init__(self, producer_id: int, topics: List[Topic]):
        """
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param topics: Errors per partition from writing markers.
        :type topics: List[Topic]
        """
        self.producer_id = producer_id
        self.topics = topics


class WriteTxnMarkersResponseData(ResponseData):

    transaction_markers: List[TransactionMarker]
    api_key: ClassVar[ApiKey] = ApiKey.WRITE_TXN_MARKERS

    def __init__(self, transaction_markers: List[TransactionMarker]):
        """
        :param transaction_markers: Errors per partition from writing markers.
        :type transaction_markers: List[TransactionMarker]
        """
        self.transaction_markers = transaction_markers
