from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class DeleteGroupsRequestData(RequestData):

    groups: List[str]
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_GROUPS

    def __init__(self, groups: List[str]):
        """
        :param groups: An array of groups to be deleted.
        :type groups: List[str]
        """
        self.groups = groups
