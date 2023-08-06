from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition: int
    offset: int

    def __init__(self, partition: int, offset: int):
        """
        :param partition: Topic partition id
        :type partition: int
        :param offset: The offset before which the messages will be deleted. -1 means high-watermark for the partition.
        :type offset: int
        """
        self.partition = partition
        self.offset = offset


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


class DeleteRecordsRequestData(RequestData):

    topics: List[Topic]
    timeout: int
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_RECORDS

    def __init__(self, topics: List[Topic], timeout: int):
        """
        :param topics: None
        :type topics: List[Topic]
        :param timeout: The maximum time to await a response in ms.
        :type timeout: int
        """
        self.topics = topics
        self.timeout = timeout
