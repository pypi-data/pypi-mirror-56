from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class ListGroupsRequestData(RequestData):

    api_key: ClassVar[ApiKey] = ApiKey.LIST_GROUPS

    def __init__(self):
        """
        """
