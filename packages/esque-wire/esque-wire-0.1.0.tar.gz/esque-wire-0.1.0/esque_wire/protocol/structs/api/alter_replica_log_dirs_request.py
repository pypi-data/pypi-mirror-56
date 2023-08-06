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


class LogDir:

    log_dir: str
    topics: List[Topic]

    def __init__(self, log_dir: str, topics: List[Topic]):
        """
        :param log_dir: The absolute log directory path.
        :type log_dir: str
        :param topics: None
        :type topics: List[Topic]
        """
        self.log_dir = log_dir
        self.topics = topics


class AlterReplicaLogDirsRequestData(RequestData):

    log_dirs: List[LogDir]
    api_key: ClassVar[ApiKey] = ApiKey.ALTER_REPLICA_LOG_DIRS

    def __init__(self, log_dirs: List[LogDir]):
        """
        :param log_dirs: None
        :type log_dirs: List[LogDir]
        """
        self.log_dirs = log_dirs
