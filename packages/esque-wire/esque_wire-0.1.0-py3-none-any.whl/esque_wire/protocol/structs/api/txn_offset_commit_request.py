from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition: int
    offset: int
    leader_epoch: int
    metadata: Optional[str]

    def __init__(self, partition: int, offset: int, leader_epoch: int, metadata: Optional[str]):
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
        """
        self.partition = partition
        self.offset = offset
        self.leader_epoch = leader_epoch
        self.metadata = metadata


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Partitions to commit offsets
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class TxnOffsetCommitRequestData(RequestData):

    transactional_id: str
    group_id: str
    producer_id: int
    producer_epoch: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.TXN_OFFSET_COMMIT

    def __init__(
        self, transactional_id: str, group_id: str, producer_id: int, producer_epoch: int, topics: List[Topic]
    ):
        """
        :param transactional_id: The transactional id corresponding to the transaction.
        :type transactional_id: str
        :param group_id: The unique group identifier
        :type group_id: str
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param producer_epoch: Current epoch associated with the producer id.
        :type producer_epoch: int
        :param topics: Topics to commit offsets
        :type topics: List[Topic]
        """
        self.transactional_id = transactional_id
        self.group_id = group_id
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
        self.topics = topics
