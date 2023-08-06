from typing import ClassVar, List, Optional

from ...constants import ApiKey, ResourceType
from ..base import RequestData


class ConfigEntry:

    config_name: str
    config_value: Optional[str]

    def __init__(self, config_name: str, config_value: Optional[str]):
        """
        :param config_name: Configuration name
        :type config_name: str
        :param config_value: Configuration value
        :type config_value: Optional[str]
        """
        self.config_name = config_name
        self.config_value = config_value


class Resource:

    resource_type: ResourceType
    resource_name: str
    config_entries: List[ConfigEntry]

    def __init__(self, resource_type: ResourceType, resource_name: str, config_entries: List[ConfigEntry]):
        """
        :param resource_type: None
        :type resource_type: ResourceType
        :param resource_name: None
        :type resource_name: str
        :param config_entries: None
        :type config_entries: List[ConfigEntry]
        """
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.config_entries = config_entries


class AlterConfigsRequestData(RequestData):

    resources: List[Resource]
    validate_only: bool
    api_key: ClassVar[ApiKey] = ApiKey.ALTER_CONFIGS

    def __init__(self, resources: List[Resource], validate_only: bool):
        """
        :param resources: An array of resources to update with the provided configs.
        :type resources: List[Resource]
        :param validate_only: None
        :type validate_only: bool
        """
        self.resources = resources
        self.validate_only = validate_only
