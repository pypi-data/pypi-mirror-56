from typing import ClassVar, List, Optional

from ...constants import AclOperation, AclPermissionType, ApiKey, ResourceType
from ..base import RequestData


class Filter:

    resource_type: ResourceType
    resource_name: Optional[str]
    resource_pattern_type_filter: int
    principal: Optional[str]
    host: Optional[str]
    operation: AclOperation
    permission_type: AclPermissionType

    def __init__(
        self,
        resource_type: ResourceType,
        resource_name: Optional[str],
        resource_pattern_type_filter: int,
        principal: Optional[str],
        host: Optional[str],
        operation: AclOperation,
        permission_type: AclPermissionType,
    ):
        """
        :param resource_type: The resource type
        :type resource_type: ResourceType
        :param resource_name: The resource name filter
        :type resource_name: Optional[str]
        :param resource_pattern_type_filter: The resource pattern type filter
        :type resource_pattern_type_filter: int
        :param principal: The ACL principal filter
        :type principal: Optional[str]
        :param host: The ACL host filter
        :type host: Optional[str]
        :param operation: The ACL operation
        :type operation: AclOperation
        :param permission_type: The ACL permission type
        :type permission_type: AclPermissionType
        """
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_pattern_type_filter = resource_pattern_type_filter
        self.principal = principal
        self.host = host
        self.operation = operation
        self.permission_type = permission_type


class DeleteAclsRequestData(RequestData):

    filters: List[Filter]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_ACLS

    def __init__(self, filters: List[Filter]):
        """
        :param filters: None
        :type filters: List[Filter]
        """
        self.filters = filters
