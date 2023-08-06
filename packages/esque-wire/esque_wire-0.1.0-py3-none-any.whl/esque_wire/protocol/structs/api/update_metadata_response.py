from typing import ClassVar

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class UpdateMetadataResponseData(ResponseData):

    error_code: ErrorCode
    api_key: ClassVar[ApiKey] = ApiKey.UPDATE_METADATA

    def __init__(self, error_code: ErrorCode):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        """
        self.error_code = error_code
