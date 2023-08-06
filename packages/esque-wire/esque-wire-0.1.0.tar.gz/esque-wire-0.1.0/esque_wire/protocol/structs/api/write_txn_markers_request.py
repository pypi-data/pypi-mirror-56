from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Topic:

    topic: str
    partitions: List[int]

    def __init__(self, topic: str, partitions: List[int]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: None
        :type partitions: List[int]
        """
        self.topic = topic
        self.partitions = partitions


class TransactionMarker:

    producer_id: int
    producer_epoch: int
    transaction_result: bool
    topics: List[Topic]
    coordinator_epoch: int

    def __init__(
        self,
        producer_id: int,
        producer_epoch: int,
        transaction_result: bool,
        topics: List[Topic],
        coordinator_epoch: int,
    ):
        """
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param producer_epoch: Current epoch associated with the producer id.
        :type producer_epoch: int
        :param transaction_result: The result of the transaction to write to the partitions (false = ABORT, true =
                                   COMMIT).
        :type transaction_result: bool
        :param topics: The partitions to write markers for.
        :type topics: List[Topic]
        :param coordinator_epoch: Epoch associated with the transaction state partition hosted by this transaction
                                  coordinator
        :type coordinator_epoch: int
        """
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
        self.transaction_result = transaction_result
        self.topics = topics
        self.coordinator_epoch = coordinator_epoch


class WriteTxnMarkersRequestData(RequestData):

    transaction_markers: List[TransactionMarker]
    api_key: ClassVar[ApiKey] = ApiKey.WRITE_TXN_MARKERS

    def __init__(self, transaction_markers: List[TransactionMarker]):
        """
        :param transaction_markers: The transaction markers to be written.
        :type transaction_markers: List[TransactionMarker]
        """
        self.transaction_markers = transaction_markers
