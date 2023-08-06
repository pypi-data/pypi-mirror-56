from typing import ClassVar, List, Optional

from ...constants import AclOperation, AclPermissionType, ApiKey, ErrorCode, ResourceType
from ..base import ResponseData


class MatchingAcl:

    error_code: ErrorCode
    error_message: Optional[str]
    resource_type: ResourceType
    resource_name: str
    resource_pattern_type: int
    principal: str
    host: str
    operation: AclOperation
    permission_type: AclPermissionType

    def __init__(
        self,
        error_code: ErrorCode,
        error_message: Optional[str],
        resource_type: ResourceType,
        resource_name: str,
        resource_pattern_type: int,
        principal: str,
        host: str,
        operation: AclOperation,
        permission_type: AclPermissionType,
    ):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        :param resource_type: The resource type
        :type resource_type: ResourceType
        :param resource_name: The resource name
        :type resource_name: str
        :param resource_pattern_type: The resource pattern type
        :type resource_pattern_type: int
        :param principal: The ACL principal
        :type principal: str
        :param host: The ACL host
        :type host: str
        :param operation: The ACL operation
        :type operation: AclOperation
        :param permission_type: The ACL permission type
        :type permission_type: AclPermissionType
        """
        self.error_code = error_code
        self.error_message = error_message
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_pattern_type = resource_pattern_type
        self.principal = principal
        self.host = host
        self.operation = operation
        self.permission_type = permission_type


class FilterResponse:

    error_code: ErrorCode
    error_message: Optional[str]
    matching_acls: List[MatchingAcl]

    def __init__(self, error_code: ErrorCode, error_message: Optional[str], matching_acls: List[MatchingAcl]):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        :param matching_acls: The matching ACLs
        :type matching_acls: List[MatchingAcl]
        """
        self.error_code = error_code
        self.error_message = error_message
        self.matching_acls = matching_acls


class DeleteAclsResponseData(ResponseData):

    throttle_time_ms: int
    filter_responses: List[FilterResponse]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_ACLS

    def __init__(self, throttle_time_ms: int, filter_responses: List[FilterResponse]):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param filter_responses: None
        :type filter_responses: List[FilterResponse]
        """
        self.throttle_time_ms = throttle_time_ms
        self.filter_responses = filter_responses
