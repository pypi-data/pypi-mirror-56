from typing import ClassVar, Optional

from ...constants import ApiKey
from ..base import RequestData


class HeartbeatRequestData(RequestData):

    group_id: str
    generation_id: int
    member_id: str
    group_instance_id: Optional[str]
    api_key: ClassVar[ApiKey] = ApiKey.HEARTBEAT

    def __init__(self, group_id: str, generation_id: int, member_id: str, group_instance_id: Optional[str]):
        """
        :param group_id: The group id.
        :type group_id: str
        :param generation_id: The generation of the group.
        :type generation_id: int
        :param member_id: The member ID.
        :type member_id: str
        :param group_instance_id: The unique identifier of the consumer instance provided by end user.
        :type group_instance_id: Optional[str]
        """
        self.group_id = group_id
        self.generation_id = generation_id
        self.member_id = member_id
        self.group_instance_id = group_instance_id
