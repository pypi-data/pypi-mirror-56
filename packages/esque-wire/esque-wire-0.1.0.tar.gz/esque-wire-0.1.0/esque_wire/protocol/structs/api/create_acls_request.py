from typing import ClassVar, List

from ...constants import AclOperation, AclPermissionType, ApiKey, ResourceType
from ..base import RequestData


class Creation:

    resource_type: ResourceType
    resource_name: str
    resource_pattern_type: int
    principal: str
    host: str
    operation: AclOperation
    permission_type: AclPermissionType

    def __init__(
        self,
        resource_type: ResourceType,
        resource_name: str,
        resource_pattern_type: int,
        principal: str,
        host: str,
        operation: AclOperation,
        permission_type: AclPermissionType,
    ):
        """
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
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_pattern_type = resource_pattern_type
        self.principal = principal
        self.host = host
        self.operation = operation
        self.permission_type = permission_type


class CreateAclsRequestData(RequestData):

    creations: List[Creation]
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_ACLS

    def __init__(self, creations: List[Creation]):
        """
        :param creations: None
        :type creations: List[Creation]
        """
        self.creations = creations
