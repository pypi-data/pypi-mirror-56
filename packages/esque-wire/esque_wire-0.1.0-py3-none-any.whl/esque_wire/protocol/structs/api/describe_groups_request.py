from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class DescribeGroupsRequestData(RequestData):

    groups: List[str]
    include_authorized_operations: bool
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_GROUPS

    def __init__(self, groups: List[str], include_authorized_operations: bool):
        """
        :param groups: The names of the groups to describe
        :type groups: List[str]
        :param include_authorized_operations: Whether to include authorized operations.
        :type include_authorized_operations: bool
        """
        self.groups = groups
        self.include_authorized_operations = include_authorized_operations
