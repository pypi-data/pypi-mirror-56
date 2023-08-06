from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition: int
    current_leader_epoch: int
    leader_epoch: int

    def __init__(self, partition: int, current_leader_epoch: int, leader_epoch: int):
        """
        :param partition: Topic partition id
        :type partition: int
        :param current_leader_epoch: The current leader epoch, if provided, is used to fence consumers/replicas with
                                     old metadata. If the epoch provided by the client is larger than the current epoch
                                     known to the broker, then the UNKNOWN_LEADER_EPOCH error code will be returned. If
                                     the provided epoch is smaller, then the FENCED_LEADER_EPOCH error code will be
                                     returned.
        :type current_leader_epoch: int
        :param leader_epoch: The epoch to lookup an offset for.
        :type leader_epoch: int
        """
        self.partition = partition
        self.current_leader_epoch = current_leader_epoch
        self.leader_epoch = leader_epoch


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: An array of partitions to get epochs for
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class OffsetForLeaderEpochRequestData(RequestData):

    replica_id: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_FOR_LEADER_EPOCH

    def __init__(self, replica_id: int, topics: List[Topic]):
        """
        :param replica_id: Broker id of the follower. For normal consumers, use -1.
        :type replica_id: int
        :param topics: An array of topics to get epochs for
        :type topics: List[Topic]
        """
        self.replica_id = replica_id
        self.topics = topics
