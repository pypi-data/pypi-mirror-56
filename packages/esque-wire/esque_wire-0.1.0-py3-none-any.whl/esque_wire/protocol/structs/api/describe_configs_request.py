from typing import ClassVar, List

from ...constants import ApiKey, ResourceType
from ..base import RequestData


class Resource:

    resource_type: ResourceType
    resource_name: str
    config_names: List[str]

    def __init__(self, resource_type: ResourceType, resource_name: str, config_names: List[str]):
        """
        :param resource_type: None
        :type resource_type: ResourceType
        :param resource_name: None
        :type resource_name: str
        :param config_names: None
        :type config_names: List[str]
        """
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.config_names = config_names


class DescribeConfigsRequestData(RequestData):

    resources: List[Resource]
    include_synonyms: bool
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_CONFIGS

    def __init__(self, resources: List[Resource], include_synonyms: bool):
        """
        :param resources: An array of config resources to be returned.
        :type resources: List[Resource]
        :param include_synonyms: None
        :type include_synonyms: bool
        """
        self.resources = resources
        self.include_synonyms = include_synonyms
