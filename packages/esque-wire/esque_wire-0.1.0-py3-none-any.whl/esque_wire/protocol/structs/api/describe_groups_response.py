from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Member:

    member_id: str
    client_id: str
    client_host: str
    member_metadata: bytes
    member_assignment: bytes

    def __init__(
        self, member_id: str, client_id: str, client_host: str, member_metadata: bytes, member_assignment: bytes
    ):
        """
        :param member_id: The member ID assigned by the group coordinator.
        :type member_id: str
        :param client_id: The client ID used in the member's latest join group request.
        :type client_id: str
        :param client_host: The client host.
        :type client_host: str
        :param member_metadata: The metadata corresponding to the current group protocol in use.
        :type member_metadata: bytes
        :param member_assignment: The current assignment provided by the group leader.
        :type member_assignment: bytes
        """
        self.member_id = member_id
        self.client_id = client_id
        self.client_host = client_host
        self.member_metadata = member_metadata
        self.member_assignment = member_assignment


class Group:

    error_code: ErrorCode
    group_id: str
    group_state: str
    protocol_type: str
    protocol_data: str
    members: List[Member]
    authorized_operations: int

    def __init__(
        self,
        error_code: ErrorCode,
        group_id: str,
        group_state: str,
        protocol_type: str,
        protocol_data: str,
        members: List[Member],
        authorized_operations: int,
    ):
        """
        :param error_code: The describe error, or 0 if there was no error.
        :type error_code: ErrorCode
        :param group_id: The group ID string.
        :type group_id: str
        :param group_state: The group state string, or the empty string.
        :type group_state: str
        :param protocol_type: The group protocol type, or the empty string.
        :type protocol_type: str
        :param protocol_data: The group protocol data, or the empty string.
        :type protocol_data: str
        :param members: The group members.
        :type members: List[Member]
        :param authorized_operations: 32-bit bitfield to represent authorized operations for this group.
        :type authorized_operations: int
        """
        self.error_code = error_code
        self.group_id = group_id
        self.group_state = group_state
        self.protocol_type = protocol_type
        self.protocol_data = protocol_data
        self.members = members
        self.authorized_operations = authorized_operations


class DescribeGroupsResponseData(ResponseData):

    throttle_time_ms: int
    groups: List[Group]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_GROUPS

    def __init__(self, throttle_time_ms: int, groups: List[Group]):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param groups: Each described group.
        :type groups: List[Group]
        """
        self.throttle_time_ms = throttle_time_ms
        self.groups = groups
