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
        :param partitions: List of partition ids of the topic.
        :type partitions: List[int]
        """
        self.topic = topic
        self.partitions = partitions


class DescribeLogDirsRequestData(RequestData):

    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_LOG_DIRS

    def __init__(self, topics: List[Topic]):
        """
        :param topics: None
        :type topics: List[Topic]
        """
        self.topics = topics
