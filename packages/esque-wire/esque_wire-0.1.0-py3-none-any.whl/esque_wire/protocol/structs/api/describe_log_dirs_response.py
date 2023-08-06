from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

    partition: int
    size: int
    offset_lag: int
    is_future: bool

    def __init__(self, partition: int, size: int, offset_lag: int, is_future: bool):
        """
        :param partition: Topic partition id
        :type partition: int
        :param size: The size of the log segments of the partition in bytes.
        :type size: int
        :param offset_lag: The lag of the log's LEO w.r.t. partition's HW (if it is the current log for the partition)
                           or current replica's LEO (if it is the future log for the partition)
        :type offset_lag: int
        :param is_future: True if this log is created by AlterReplicaLogDirsRequest and will replace the current log of
                          the replica in the future.
        :type is_future: bool
        """
        self.partition = partition
        self.size = size
        self.offset_lag = offset_lag
        self.is_future = is_future


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


class LogDir:

    error_code: ErrorCode
    log_dir: str
    topics: List[Topic]

    def __init__(self, error_code: ErrorCode, log_dir: str, topics: List[Topic]):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param log_dir: The absolute log directory path.
        :type log_dir: str
        :param topics: None
        :type topics: List[Topic]
        """
        self.error_code = error_code
        self.log_dir = log_dir
        self.topics = topics


class DescribeLogDirsResponseData(ResponseData):

    throttle_time_ms: int
    log_dirs: List[LogDir]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_LOG_DIRS

    def __init__(self, throttle_time_ms: int, log_dirs: List[LogDir]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param log_dirs: None
        :type log_dirs: List[LogDir]
        """
        self.throttle_time_ms = throttle_time_ms
        self.log_dirs = log_dirs
