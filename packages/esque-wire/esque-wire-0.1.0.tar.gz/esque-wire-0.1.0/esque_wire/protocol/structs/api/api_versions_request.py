from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class ApiVersionsRequestData(RequestData):

    api_key: ClassVar[ApiKey] = ApiKey.API_VERSIONS

    def __init__(self):
        """
        """
