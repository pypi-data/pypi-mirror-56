from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class LeaveGroupRequestData(RequestData):

    group_id: str
    member_id: str
    api_key: ClassVar[ApiKey] = ApiKey.LEAVE_GROUP

    def __init__(self, group_id: str, member_id: str):
        """
        :param group_id: The ID of the group to leave.
        :type group_id: str
        :param member_id: The member ID to remove from the group.
        :type member_id: str
        """
        self.group_id = group_id
        self.member_id = member_id
