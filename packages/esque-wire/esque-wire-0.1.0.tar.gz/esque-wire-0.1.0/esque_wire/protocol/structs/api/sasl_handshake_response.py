from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class SaslHandshakeResponseData(ResponseData):

    error_code: ErrorCode
    mechanisms: List[str]
    api_key: ClassVar[ApiKey] = ApiKey.SASL_HANDSHAKE

    def __init__(self, error_code: ErrorCode, mechanisms: List[str]):
        """
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param mechanisms: The mechanisms enabled in the server.
        :type mechanisms: List[str]
        """
        self.error_code = error_code
        self.mechanisms = mechanisms
