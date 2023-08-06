from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    partition_index: int
    committed_offset: int
    committed_leader_epoch: int
    committed_metadata: Optional[str]

    def __init__(
        self,
        partition_index: int,
        committed_offset: int,
        committed_leader_epoch: int,
        committed_metadata: Optional[str],
    ):
        """
        :param partition_index: The partition index.
        :type partition_index: int
        :param committed_offset: The message offset to be committed.
        :type committed_offset: int
        :param committed_leader_epoch: The leader epoch of this partition.
        :type committed_leader_epoch: int
        :param committed_metadata: Any associated metadata the client wants to keep.
        :type committed_metadata: Optional[str]
        """
        self.partition_index = partition_index
        self.committed_offset = committed_offset
        self.committed_leader_epoch = committed_leader_epoch
        self.committed_metadata = committed_metadata


class Topic:

    name: str
    partitions: List[Partition]

    def __init__(self, name: str, partitions: List[Partition]):
        """
        :param name: The topic name.
        :type name: str
        :param partitions: Each partition to commit offsets for.
        :type partitions: List[Partition]
        """
        self.name = name
        self.partitions = partitions


class OffsetCommitRequestData(RequestData):

    group_id: str
    generation_id: int
    member_id: str
    group_instance_id: Optional[str]
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.OFFSET_COMMIT

    def __init__(
        self, group_id: str, generation_id: int, member_id: str, group_instance_id: Optional[str], topics: List[Topic]
    ):
        """
        :param group_id: The unique group identifier.
        :type group_id: str
        :param generation_id: The generation of the group.
        :type generation_id: int
        :param member_id: The member ID assigned by the group coordinator.
        :type member_id: str
        :param group_instance_id: The unique identifier of the consumer instance provided by end user.
        :type group_instance_id: Optional[str]
        :param topics: The topics to commit offsets for.
        :type topics: List[Topic]
        """
        self.group_id = group_id
        self.generation_id = generation_id
        self.member_id = member_id
        self.group_instance_id = group_instance_id
        self.topics = topics
