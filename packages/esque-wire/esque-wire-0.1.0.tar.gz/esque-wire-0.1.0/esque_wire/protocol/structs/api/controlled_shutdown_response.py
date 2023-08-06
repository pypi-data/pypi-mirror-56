from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class RemainingPartition:

    topic_name: str
    partition_index: int

    def __init__(self, topic_name: str, partition_index: int):
        """
        :param topic_name: The name of the topic.
        :type topic_name: str
        :param partition_index: The index of the partition.
        :type partition_index: int
        """
        self.topic_name = topic_name
        self.partition_index = partition_index


class ControlledShutdownResponseData(ResponseData):

    error_code: ErrorCode
    remaining_partitions: List[RemainingPartition]
    api_key: ClassVar[ApiKey] = ApiKey.CONTROLLED_SHUTDOWN

    def __init__(self, error_code: ErrorCode, remaining_partitions: List[RemainingPartition]):
        """
        :param error_code: The top-level error code.
        :type error_code: ErrorCode
        :param remaining_partitions: The partitions that the broker still leads.
        :type remaining_partitions: List[RemainingPartition]
        """
        self.error_code = error_code
        self.remaining_partitions = remaining_partitions
