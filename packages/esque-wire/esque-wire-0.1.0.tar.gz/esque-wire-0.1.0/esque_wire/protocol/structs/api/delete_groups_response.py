from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class GroupErrorCode:

    group_id: str
    error_code: ErrorCode

    def __init__(self, group_id: str, error_code: ErrorCode):
        """
        :param group_id: The unique group identifier
        :type group_id: str
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.group_id = group_id
        self.error_code = error_code


class DeleteGroupsResponseData(ResponseData):

    throttle_time_ms: int
    group_error_codes: List[GroupErrorCode]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_GROUPS

    def __init__(self, throttle_time_ms: int, group_error_codes: List[GroupErrorCode]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param group_error_codes: An array of per group error codes.
        :type group_error_codes: List[GroupErrorCode]
        """
        self.throttle_time_ms = throttle_time_ms
        self.group_error_codes = group_error_codes
