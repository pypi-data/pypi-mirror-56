from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition: int
    current_leader_epoch: int
    timestamp: int

    def __init__(self, partition: int, current_leader_epoch: int, timestamp: int):
        """
        :param partition: Topic partition id
        :type partition: int
        :param current_leader_epoch: The current leader epoch, if provided, is used to fence consumers/replicas with
                                     old metadata. If the epoch provided by the client is larger than the current epoch
                                     known to the broker, then the UNKNOWN_LEADER_EPOCH error code will be returned. If
                                     the provided epoch is smaller, then the FENCED_LEADER_EPOCH error code will be
                                     returned.
        :type current_leader_epoch: int
        :param timestamp: The target timestamp for the partition.
        :type timestamp: int
        """
        self.partition = partition
        self.current_leader_epoch = current_leader_epoch
        self.timestamp = timestamp


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Partitions to list offsets.
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class ListOffsetsRequestData(RequestData):

    replica_id: int
    isolation_level: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.LIST_OFFSETS

    def __init__(self, replica_id: int, isolation_level: int, topics: List[Topic]):
        """
        :param replica_id: Broker id of the follower. For normal consumers, use -1.
        :type replica_id: int
        :param isolation_level: This setting controls the visibility of transactional records. Using READ_UNCOMMITTED
                                (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level =
                                1), non-transactional and COMMITTED transactional records are visible. To be more
                                concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO
                                (last stable offset), and enables the inclusion of the list of aborted transactions in
                                the result, which allows consumers to discard ABORTED transactional records
        :type isolation_level: int
        :param topics: Topics to list offsets.
        :type topics: List[Topic]
        """
        self.replica_id = replica_id
        self.isolation_level = isolation_level
        self.topics = topics
