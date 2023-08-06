from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class TopicPartition:

    topic: str
    partition_id: List[int]

    def __init__(self, topic: str, partition_id: List[int]):
        """
        :param topic: The name of a topic.
        :type topic: str
        :param partition_id: The partitions of this topic whose preferred leader should be elected
        :type partition_id: List[int]
        """
        self.topic = topic
        self.partition_id = partition_id


class ElectPreferredLeadersRequestData(RequestData):

    topic_partitions: List[TopicPartition]
    timeout_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.ELECT_PREFERRED_LEADERS

    def __init__(self, topic_partitions: List[TopicPartition], timeout_ms: int):
        """
        :param topic_partitions: The topic partitions to elect the preferred leader of.
        :type topic_partitions: List[TopicPartition]
        :param timeout_ms: The time in ms to wait for the election to complete.
        :type timeout_ms: int
        """
        self.topic_partitions = topic_partitions
        self.timeout_ms = timeout_ms
