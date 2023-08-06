from typing import ClassVar, List, Optional

from ...constants import AclOperation, AclPermissionType, ApiKey, ErrorCode, ResourceType
from ..base import ResponseData


class Acl:

    principal: str
    host: str
    operation: AclOperation
    permission_type: AclPermissionType

    def __init__(self, principal: str, host: str, operation: AclOperation, permission_type: AclPermissionType):
        """
        :param principal: The ACL principal
        :type principal: str
        :param host: The ACL host
        :type host: str
        :param operation: The ACL operation
        :type operation: AclOperation
        :param permission_type: The ACL permission type
        :type permission_type: AclPermissionType
        """
        self.principal = principal
        self.host = host
        self.operation = operation
        self.permission_type = permission_type


class Resource:

    resource_type: ResourceType
    resource_name: str
    resource_pattern_type: int
    acls: List[Acl]

    def __init__(self, resource_type: ResourceType, resource_name: str, resource_pattern_type: int, acls: List[Acl]):
        """
        :param resource_type: The resource type
        :type resource_type: ResourceType
        :param resource_name: The resource name
        :type resource_name: str
        :param resource_pattern_type: The resource pattern type
        :type resource_pattern_type: int
        :param acls: None
        :type acls: List[Acl]
        """
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_pattern_type = resource_pattern_type
        self.acls = acls


class DescribeAclsResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    error_message: Optional[str]
    resources: List[Resource]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_ACLS

    def __init__(
        self, throttle_time_ms: int, error_code: ErrorCode, error_message: Optional[str], resources: List[Resource]
    ):
        """
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param error_message: Response error message
        :type error_message: Optional[str]
        :param resources: The resources and their associated ACLs.
        :type resources: List[Resource]
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.error_message = error_message
        self.resources = resources
