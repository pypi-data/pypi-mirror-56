from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Topic:

    name: str

    def __init__(self, name: str):
        """
        :param name: The topic name.
        :type name: str
        """
        self.name = name


class MetadataRequestData(RequestData):

    topics: List[Topic]
    allow_auto_topic_creation: bool
    include_cluster_authorized_operations: bool
    include_topic_authorized_operations: bool
    api_key: ClassVar[ApiKey] = ApiKey.METADATA

    def __init__(
        self,
        topics: List[Topic],
        allow_auto_topic_creation: bool,
        include_cluster_authorized_operations: bool,
        include_topic_authorized_operations: bool,
    ):
        """
        :param topics: The topics to fetch metadata for.
        :type topics: List[Topic]
        :param allow_auto_topic_creation: If this is true, the broker may auto-create topics that we requested which do
                                          not already exist, if it is configured to do so.
        :type allow_auto_topic_creation: bool
        :param include_cluster_authorized_operations: Whether to include cluster authorized operations.
        :type include_cluster_authorized_operations: bool
        :param include_topic_authorized_operations: Whether to include topic authorized operations.
        :type include_topic_authorized_operations: bool
        """
        self.topics = topics
        self.allow_auto_topic_creation = allow_auto_topic_creation
        self.include_cluster_authorized_operations = include_cluster_authorized_operations
        self.include_topic_authorized_operations = include_topic_authorized_operations
