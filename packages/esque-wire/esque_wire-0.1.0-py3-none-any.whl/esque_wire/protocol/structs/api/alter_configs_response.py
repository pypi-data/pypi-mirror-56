from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode, ResourceType
from ..base import ResponseData


class Resource:

    error_code: ErrorCode
    error_message: Optional[str]
    resource_type: ResourceType
    resource_name: str

    def __init__(
        self, error_code: ErrorCode, error_message: Optional[str], resource_type: ResourceType, resource_name: str
    ):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        :param resource_type: None
        :type resource_type: ResourceType
        :param resource_name: None
        :type resource_name: str
        """
        self.error_code = error_code
        self.error_message = error_message
        self.resource_type = resource_type
        self.resource_name = resource_name


class AlterConfigsResponseData(ResponseData):

    throttle_time_ms: int
    resources: List[Resource]
    api_key: ClassVar[ApiKey] = ApiKey.ALTER_CONFIGS

    def __init__(self, throttle_time_ms: int, resources: List[Resource]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param resources: None
        :type resources: List[Resource]
        """
        self.throttle_time_ms = throttle_time_ms
        self.resources = resources
