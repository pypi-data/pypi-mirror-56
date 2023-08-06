from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class CreationResponse:

    error_code: ErrorCode
    error_message: Optional[str]

    def __init__(self, error_code: ErrorCode, error_message: Optional[str]):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        """
        self.error_code = error_code
        self.error_message = error_message


class CreateAclsResponseData(ResponseData):

    throttle_time_ms: int
    creation_responses: List[CreationResponse]
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_ACLS

    def __init__(self, throttle_time_ms: int, creation_responses: List[CreationResponse]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param creation_responses: None
        :type creation_responses: List[CreationResponse]
        """
        self.throttle_time_ms = throttle_time_ms
        self.creation_responses = creation_responses
