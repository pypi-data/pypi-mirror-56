from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Topic:

    name: str
    error_code: ErrorCode
    error_message: Optional[str]

    def __init__(self, name: str, error_code: ErrorCode, error_message: Optional[str]):
        """
        :param name: The topic name.
        :type name: str
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param error_message: The error message, or null if there was no error.
        :type error_message: Optional[str]
        """
        self.name = name
        self.error_code = error_code
        self.error_message = error_message


class CreateTopicsResponseData(ResponseData):

    throttle_time_ms: int
    topics: List[Topic]
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_TOPICS

    def __init__(self, throttle_time_ms: int, topics: List[Topic]):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param topics: Results for each topic we tried to create.
        :type topics: List[Topic]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topics = topics
