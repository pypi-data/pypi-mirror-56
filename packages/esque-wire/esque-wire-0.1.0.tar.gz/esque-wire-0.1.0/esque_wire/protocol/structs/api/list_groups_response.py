from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Group:

    group_id: str
    protocol_type: str

    def __init__(self, group_id: str, protocol_type: str):
        """
        :param group_id: The unique group identifier
        :type group_id: str
        :param protocol_type: None
        :type protocol_type: str
        """
        self.group_id = group_id
        self.protocol_type = protocol_type


class ListGroupsResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    groups: List[Group]
    api_key: ClassVar[ApiKey] = ApiKey.LIST_GROUPS

    def __init__(self, throttle_time_ms: int, error_code: ErrorCode, groups: List[Group]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param groups: None
        :type groups: List[Group]
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.groups = groups
