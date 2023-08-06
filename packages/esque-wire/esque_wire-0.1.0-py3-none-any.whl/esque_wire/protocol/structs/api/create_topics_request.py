from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Config:

    name: str
    value: Optional[str]

    def __init__(self, name: str, value: Optional[str]):
        """
        :param name: The configuration name.
        :type name: str
        :param value: The configuration value.
        :type value: Optional[str]
        """
        self.name = name
        self.value = value


class Assignment:

    partition_index: int
    broker_ids: List[int]

    def __init__(self, partition_index: int, broker_ids: List[int]):
        """
        :param partition_index: The partition index.
        :type partition_index: int
        :param broker_ids: The brokers to place the partition on.
        :type broker_ids: List[int]
        """
        self.partition_index = partition_index
        self.broker_ids = broker_ids


class Topic:

    name: str
    num_partitions: int
    replication_factor: int
    assignments: List[Assignment]
    configs: List[Config]

    def __init__(
        self,
        name: str,
        num_partitions: int,
        replication_factor: int,
        assignments: List[Assignment],
        configs: List[Config],
    ):
        """
        :param name: The topic name.
        :type name: str
        :param num_partitions: The number of partitions to create in the topic, or -1 if we are specifying a manual
                               partition assignment.
        :type num_partitions: int
        :param replication_factor: The number of replicas to create for each partition in the topic, or -1 if we are
                                   specifying a manual partition assignment.
        :type replication_factor: int
        :param assignments: The manual partition assignment, or the empty array if we are using automatic assignment.
        :type assignments: List[Assignment]
        :param configs: The custom topic configurations to set.
        :type configs: List[Config]
        """
        self.name = name
        self.num_partitions = num_partitions
        self.replication_factor = replication_factor
        self.assignments = assignments
        self.configs = configs


class CreateTopicsRequestData(RequestData):

    topics: List[Topic]
    timeout_ms: int
    validate_only: bool
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_TOPICS

    def __init__(self, topics: List[Topic], timeout_ms: int, validate_only: bool):
        """
        :param topics: The topics to create.
        :type topics: List[Topic]
        :param timeout_ms: How long to wait in milliseconds before timing out the request.
        :type timeout_ms: int
        :param validate_only: If true, check that the topics can be created as specified, but don't create anything.
        :type validate_only: bool
        """
        self.topics = topics
        self.timeout_ms = timeout_ms
        self.validate_only = validate_only
