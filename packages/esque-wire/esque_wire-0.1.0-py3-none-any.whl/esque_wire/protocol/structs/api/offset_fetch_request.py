from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition: int

    def __init__(self, partition: int):
        """
        :param partition: Topic partition id
        :type partition: int
        """
        self.partition = partition


class Topic:

    topic: str
    partitions: List[Partition]

    def __init__(self, topic: str, partitions: List[Partition]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partitions: Partitions to fetch offsets.
        :type partitions: List[Partition]
        """
        self.topic = topic
        self.partitions = partitions


class OffsetFetchRequestData(RequestData):

    group_id: str
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_FETCH

    def __init__(self, group_id: str, topics: List[Topic]):
        """
        :param group_id: The unique group identifier
        :type group_id: str
        :param topics: Topics to fetch offsets. If the topic array is null fetch offsets for all topics.
        :type topics: List[Topic]
        """
        self.group_id = group_id
        self.topics = topics
