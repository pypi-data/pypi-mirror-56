from typing import ClassVar, List, Optional

from ...constants import ApiKey, ErrorCode, ResourceType
from ..base import ResponseData


class ConfigSynonym:

    config_name: str
    config_value: Optional[str]
    config_source: int

    def __init__(self, config_name: str, config_value: Optional[str], config_source: int):
        """
        :param config_name: None
        :type config_name: str
        :param config_value: None
        :type config_value: Optional[str]
        :param config_source: None
        :type config_source: int
        """
        self.config_name = config_name
        self.config_value = config_value
        self.config_source = config_source


class ConfigEntry:

    config_name: str
    config_value: Optional[str]
    read_only: bool
    config_source: int
    is_sensitive: bool
    config_synonyms: List[ConfigSynonym]

    def __init__(
        self,
        config_name: str,
        config_value: Optional[str],
        read_only: bool,
        config_source: int,
        is_sensitive: bool,
        config_synonyms: List[ConfigSynonym],
    ):
        """
        :param config_name: None
        :type config_name: str
        :param config_value: None
        :type config_value: Optional[str]
        :param read_only: None
        :type read_only: bool
        :param config_source: None
        :type config_source: int
        :param is_sensitive: None
        :type is_sensitive: bool
        :param config_synonyms: None
        :type config_synonyms: List[ConfigSynonym]
        """
        self.config_name = config_name
        self.config_value = config_value
        self.read_only = read_only
        self.config_source = config_source
        self.is_sensitive = is_sensitive
        self.config_synonyms = config_synonyms


class Resource:

    error_code: ErrorCode
    error_message: Optional[str]
    resource_type: ResourceType
    resource_name: str
    config_entries: List[ConfigEntry]

    def __init__(
        self,
        error_code: ErrorCode,
        error_message: Optional[str],
        resource_type: ResourceType,
        resource_name: str,
        config_entries: List[ConfigEntry],
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
        :param config_entries: None
        :type config_entries: List[ConfigEntry]
        """
        self.error_code = error_code
        self.error_message = error_message
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.config_entries = config_entries


class DescribeConfigsResponseData(ResponseData):

    throttle_time_ms: int
    resources: List[Resource]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_CONFIGS

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
