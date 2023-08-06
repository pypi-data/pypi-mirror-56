from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Assignment:

    member_id: str
    assignment: bytes

    def __init__(self, member_id: str, assignment: bytes):
        """
        :param member_id: The ID of the member to assign.
        :type member_id: str
        :param assignment: The member assignment.
        :type assignment: bytes
        """
        self.member_id = member_id
        self.assignment = assignment


class SyncGroupRequestData(RequestData):

    group_id: str
    generation_id: int
    member_id: str
    group_instance_id: Optional[str]
    assignments: List[Assignment]
    api_key: ClassVar[ApiKey] = ApiKey.SYNC_GROUP

    def __init__(
        self,
        group_id: str,
        generation_id: int,
        member_id: str,
        group_instance_id: Optional[str],
        assignments: List[Assignment],
    ):
        """
        :param group_id: The unique group identifier.
        :type group_id: str
        :param generation_id: The generation of the group.
        :type generation_id: int
        :param member_id: The member ID assigned by the group.
        :type member_id: str
        :param group_instance_id: The unique identifier of the consumer instance provided by end user.
        :type group_instance_id: Optional[str]
        :param assignments: Each assignment.
        :type assignments: List[Assignment]
        """
        self.group_id = group_id
        self.generation_id = generation_id
        self.member_id = member_id
        self.group_instance_id = group_instance_id
        self.assignments = assignments
