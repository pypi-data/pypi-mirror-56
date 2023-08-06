from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Response:

    name: str
    error_code: ErrorCode

    def __init__(self, name: str, error_code: ErrorCode):
        """
        :param name: The topic name
        :type name: str
        :param error_code: The deletion error, or 0 if the deletion succeeded.
        :type error_code: ErrorCode
        """
        self.name = name
        self.error_code = error_code


class DeleteTopicsResponseData(ResponseData):

    throttle_time_ms: int
    responses: List[Response]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_TOPICS

    def __init__(self, throttle_time_ms: int, responses: List[Response]):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param responses: The results for each topic we tried to delete.
        :type responses: List[Response]
        """
        self.throttle_time_ms = throttle_time_ms
        self.responses = responses
