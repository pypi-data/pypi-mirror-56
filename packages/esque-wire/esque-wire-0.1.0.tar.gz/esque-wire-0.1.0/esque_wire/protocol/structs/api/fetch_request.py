from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class ForgottenTopicsData:

    topic: str
    partitions: List[int]

    def __init__(self, topic: str, partitions: List[int]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Partitions to remove from the fetch session.
        :type partitions: List[int]
        """
        self.topic = topic
        self.partitions = partitions


class Partition:

    partition: int
    current_leader_epoch: int
    fetch_offset: int
    log_start_offset: int
    partition_max_bytes: int

    def __init__(
        self,
        partition: int,
        current_leader_epoch: int,
        fetch_offset: int,
        log_start_offset: int,
        partition_max_bytes: int,
    ):
        """
        :param partition: Topic partition id
        :type partition: int
        :param current_leader_epoch: The current leader epoch, if provided, is used to fence consumers/replicas with
                                     old metadata. If the epoch provided by the client is larger than the current epoch
                                     known to the broker, then the UNKNOWN_LEADER_EPOCH error code will be returned. If
                                     the provided epoch is smaller, then the FENCED_LEADER_EPOCH error code will be
                                     returned.
        :type current_leader_epoch: int
        :param fetch_offset: Message offset.
        :type fetch_offset: int
        :param log_start_offset: Earliest available offset of the follower replica. The field is only used when request
                                 is sent by follower.
        :type log_start_offset: int
        :param partition_max_bytes: Maximum bytes to fetch.
        :type partition_max_bytes: int
        """
        self.partition = partition
        self.current_leader_epoch = current_leader_epoch
        self.fetch_offset = fetch_offset
        self.log_start_offset = log_start_offset
        self.partition_max_bytes = partition_max_bytes


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Partitions to fetch.
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class FetchRequestData(RequestData):

    replica_id: int
    max_wait_time: int
    min_bytes: int
    max_bytes: int
    isolation_level: int
    session_id: int
    session_epoch: int
    topics: List[Topic]
    forgotten_topics_data: List[ForgottenTopicsData]
    rack_id: str
    api_key: ClassVar[ApiKey] = ApiKey.FETCH

    def __init__(
        self,
        replica_id: int,
        max_wait_time: int,
        min_bytes: int,
        max_bytes: int,
        isolation_level: int,
        session_id: int,
        session_epoch: int,
        topics: List[Topic],
        forgotten_topics_data: List[ForgottenTopicsData],
        rack_id: str,
    ):
        """
        :param replica_id: Broker id of the follower. For normal consumers, use -1.
        :type replica_id: int
        :param max_wait_time: Maximum time in ms to wait for the response.
        :type max_wait_time: int
        :param min_bytes: Minimum bytes to accumulate in the response.
        :type min_bytes: int
        :param max_bytes: Maximum bytes to accumulate in the response. Note that this is not an absolute maximum, if
                          the first message in the first non-empty partition of the fetch is larger than this value,
                          the message will still be returned to ensure that progress can be made.
        :type max_bytes: int
        :param isolation_level: This setting controls the visibility of transactional records. Using READ_UNCOMMITTED
                                (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level =
                                1), non-transactional and COMMITTED transactional records are visible. To be more
                                concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO
                                (last stable offset), and enables the inclusion of the list of aborted transactions in
                                the result, which allows consumers to discard ABORTED transactional records
        :type isolation_level: int
        :param session_id: The fetch session ID
        :type session_id: int
        :param session_epoch: The fetch session epoch
        :type session_epoch: int
        :param topics: Topics to fetch in the order provided.
        :type topics: List[Topic]
        :param forgotten_topics_data: Topics to remove from the fetch session.
        :type forgotten_topics_data: List[ForgottenTopicsData]
        :param rack_id: The consumer's rack id
        :type rack_id: str
        """
        self.replica_id = replica_id
        self.max_wait_time = max_wait_time
        self.min_bytes = min_bytes
        self.max_bytes = max_bytes
        self.isolation_level = isolation_level
        self.session_id = session_id
        self.session_epoch = session_epoch
        self.topics = topics
        self.forgotten_topics_data = forgotten_topics_data
        self.rack_id = rack_id
