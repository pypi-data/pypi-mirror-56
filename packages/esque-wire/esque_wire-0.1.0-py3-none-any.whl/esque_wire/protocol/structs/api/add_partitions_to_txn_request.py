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


class AddPartitionsToTxnRequestData(RequestData):

    transactional_id: str
    producer_id: int
    producer_epoch: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.ADD_PARTITIONS_TO_TXN

    def __init__(self, transactional_id: str, producer_id: int, producer_epoch: int, topics: List[Topic]):
        """
        :param transactional_id: The transactional id corresponding to the transaction.
        :type transactional_id: str
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param producer_epoch: Current epoch associated with the producer id.
        :type producer_epoch: int
        :param topics: The partitions to add to the transaction.
        :type topics: List[Topic]
        """
        self.transactional_id = transactional_id
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
        self.topics = topics
