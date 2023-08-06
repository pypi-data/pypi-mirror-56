from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode, ResourceType
from ..base import ResponseData


class Response:

    error_code: ErrorCode
    error_message: Optional[str]
    resource_type: ResourceType
    resource_name: str

    def __init__(
        self, error_code: ErrorCode, error_message: Optional[str], resource_type: ResourceType, resource_name: str
    ):
        """
        :param error_code: The resource error code.
        :type error_code: ErrorCode
        :param error_message: The resource error message, or null if there was no error.
        :type error_message: Optional[str]
        :param resource_type: The resource type.
        :type resource_type: ResourceType
        :param resource_name: The resource name.
        :type resource_name: str
        """
        self.error_code = error_code
        self.error_message = error_message
        self.resource_type = resource_type
        self.resource_name = resource_name


class IncrementalAlterConfigsResponseData(ResponseData):

    throttle_time_ms: int
    responses: List[Response]
    api_key: ClassVar[ApiKey] = ApiKey.INCREMENTAL_ALTER_CONFIGS

    def __init__(self, throttle_time_ms: int, responses: List[Response]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to a quota violation,
                                 or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param responses: The responses for each resource.
        :type responses: List[Response]
        """
        self.throttle_time_ms = throttle_time_ms
        self.responses = responses
