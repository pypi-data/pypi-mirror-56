from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class FindCoordinatorRequestData(RequestData):

    key: str
    key_type: int
    api_key: ClassVar[ApiKey] = ApiKey.FIND_COORDINATOR

    def __init__(self, key: str, key_type: int):
        """
        :param key: The coordinator key.
        :type key: str
        :param key_type: The coordinator key type.  (Group, transaction, etc.)
        :type key_type: int
        """
        self.key = key
        self.key_type = key_type
