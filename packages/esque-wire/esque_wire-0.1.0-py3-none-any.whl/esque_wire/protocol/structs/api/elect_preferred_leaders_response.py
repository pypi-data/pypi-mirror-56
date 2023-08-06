from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class PartitionResult:

    partition_id: int
    error_code: ErrorCode
    error_message: Optional[str]

    def __init__(self, partition_id: int, error_code: ErrorCode, error_message: Optional[str]):
        """
        :param partition_id: The partition id
        :type partition_id: int
        :param error_code: The result error, or zero if there was no error.
        :type error_code: ErrorCode
        :param error_message: The result message, or null if there was no error.
        :type error_message: Optional[str]
        """
        self.partition_id = partition_id
        self.error_code = error_code
        self.error_message = error_message


class ReplicaElectionResult:

    topic: str
    partition_result: List[PartitionResult]

    def __init__(self, topic: str, partition_result: List[PartitionResult]):
        """
        :param topic: The topic name
        :type topic: str
        :param partition_result: The results for each partition
        :type partition_result: List[PartitionResult]
        """
        self.topic = topic
        self.partition_result = partition_result


class ElectPreferredLeadersResponseData(ResponseData):

    throttle_time_ms: int
    replica_election_results: List[ReplicaElectionResult]
    api_key: ClassVar[ApiKey] = ApiKey.ELECT_PREFERRED_LEADERS

    def __init__(self, throttle_time_ms: int, replica_election_results: List[ReplicaElectionResult]):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param replica_election_results: The election results, or an empty array if the requester did not have
                                         permission and the request asks for all partitions.
        :type replica_election_results: List[ReplicaElectionResult]
        """
        self.throttle_time_ms = throttle_time_ms
        self.replica_election_results = replica_election_results
