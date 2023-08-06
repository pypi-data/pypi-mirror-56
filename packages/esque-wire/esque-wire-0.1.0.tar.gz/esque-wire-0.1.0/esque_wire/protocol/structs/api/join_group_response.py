from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Member:

    member_id: str
    group_instance_id: Optional[str]
    metadata: bytes

    def __init__(self, member_id: str, group_instance_id: Optional[str], metadata: bytes):
        """
        :param member_id: The group member ID.
        :type member_id: str
        :param group_instance_id: The unique identifier of the consumer instance provided by end user.
        :type group_instance_id: Optional[str]
        :param metadata: The group member metadata.
        :type metadata: bytes
        """
        self.member_id = member_id
        self.group_instance_id = group_instance_id
        self.metadata = metadata


class JoinGroupResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    generation_id: int
    protocol_name: str
    leader: str
    member_id: str
    members: List[Member]
    api_key: ClassVar[ApiKey] = ApiKey.JOIN_GROUP

    def __init__(
        self,
        throttle_time_ms: int,
        error_code: ErrorCode,
        generation_id: int,
        protocol_name: str,
        leader: str,
        member_id: str,
        members: List[Member],
    ):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param generation_id: The generation ID of the group.
        :type generation_id: int
        :param protocol_name: The group protocol selected by the coordinator.
        :type protocol_name: str
        :param leader: The leader of the group.
        :type leader: str
        :param member_id: The member ID assigned by the group coordinator.
        :type member_id: str
        :param members:
        :type members: List[Member]
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.generation_id = generation_id
        self.protocol_name = protocol_name
        self.leader = leader
        self.member_id = member_id
        self.members = members
