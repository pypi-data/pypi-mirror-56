from typing import ClassVar, List, Optional

from ...constants import ApiKey, ResourceType
from ..base import RequestData


class Config:

    name: str
    config_operation: int
    value: Optional[str]

    def __init__(self, name: str, config_operation: int, value: Optional[str]):
        """
        :param name: The configuration key name.
        :type name: str
        :param config_operation: The type (Set, Delete, Append, Subtract) of operation.
        :type config_operation: int
        :param value: The value to set for the configuration key.
        :type value: Optional[str]
        """
        self.name = name
        self.config_operation = config_operation
        self.value = value


class Resource:

    resource_type: ResourceType
    resource_name: str
    configs: List[Config]

    def __init__(self, resource_type: ResourceType, resource_name: str, configs: List[Config]):
        """
        :param resource_type: The resource type.
        :type resource_type: ResourceType
        :param resource_name: The resource name.
        :type resource_name: str
        :param configs: The configurations.
        :type configs: List[Config]
        """
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.configs = configs


class IncrementalAlterConfigsRequestData(RequestData):

    resources: List[Resource]
    validate_only: bool
    api_key: ClassVar[ApiKey] = ApiKey.INCREMENTAL_ALTER_CONFIGS

    def __init__(self, resources: List[Resource], validate_only: bool):
        """
        :param resources: The incremental updates for each resource.
        :type resources: List[Resource]
        :param validate_only: True if we should validate the request, but not change the configurations.
        :type validate_only: bool
        """
        self.resources = resources
        self.validate_only = validate_only
