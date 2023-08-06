from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class TopicError:

    topic: str
    error_code: ErrorCode
    error_message: Optional[str]

    def __init__(self, topic: str, error_code: ErrorCode, error_message: Optional[str]):
        """
        :param topic: Name of topic
        :type topic: str
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        """
        self.topic = topic
        self.error_code = error_code
        self.error_message = error_message


class CreatePartitionsResponseData(ResponseData):

    throttle_time_ms: int
    topic_errors: List[TopicError]
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_PARTITIONS

    def __init__(self, throttle_time_ms: int, topic_errors: List[TopicError]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param topic_errors: Per topic results for the create partitions request
        :type topic_errors: List[TopicError]
        """
        self.throttle_time_ms = throttle_time_ms
        self.topic_errors = topic_errors
