from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Partition:

    topic: str
    partition: int
    error_code: ErrorCode

    def __init__(self, topic: str, partition: int, error_code: ErrorCode):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition: Topic partition id
        :type partition: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.topic = topic
        self.partition = partition
        self.error_code = error_code


class LeaderAndIsrResponseData(ResponseData):

    error_code: ErrorCode
    partitions: List[Partition]
    api_key: ClassVar[ApiKey] = ApiKey.LEADER_AND_ISR

    def __init__(self, error_code: ErrorCode, partitions: List[Partition]):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param partitions: Response for the requests partitions
        :type partitions: List[Partition]
        """
        self.error_code = error_code
        self.partitions = partitions
