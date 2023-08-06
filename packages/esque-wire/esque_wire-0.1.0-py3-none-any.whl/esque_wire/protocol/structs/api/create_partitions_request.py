from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class NewPartitions:

    count: int
    assignment: List[List[int]]

    def __init__(self, count: int, assignment: List[List[int]]):
        """
        :param count: The new partition count.
        :type count: int
        :param assignment: The assigned brokers.
        :type assignment: List[List[int]]
        """
        self.count = count
        self.assignment = assignment


class TopicPartition:

    topic: str
    new_partitions: NewPartitions

    def __init__(self, topic: str, new_partitions: NewPartitions):
        """
        :param topic: Name of topic
        :type topic: str
        :param new_partitions: None
        :type new_partitions: NewPartitions
        """
        self.topic = topic
        self.new_partitions = new_partitions


class CreatePartitionsRequestData(RequestData):

    topic_partitions: List[TopicPartition]
    timeout: int
    validate_only: bool
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_PARTITIONS

    def __init__(self, topic_partitions: List[TopicPartition], timeout: int, validate_only: bool):
        """
        :param topic_partitions: List of topic and the corresponding new partitions.
        :type topic_partitions: List[TopicPartition]
        :param timeout: The time in ms to wait for the partitions to be created.
        :type timeout: int
        :param validate_only: If true then validate the request, but don't actually increase the number of partitions.
        :type validate_only: bool
        """
        self.topic_partitions = topic_partitions
        self.timeout = timeout
        self.validate_only = validate_only
