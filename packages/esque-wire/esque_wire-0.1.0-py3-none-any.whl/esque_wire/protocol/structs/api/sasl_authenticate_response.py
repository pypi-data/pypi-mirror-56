from typing import ClassVar, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class SaslAuthenticateResponseData(ResponseData):

    error_code: ErrorCode
    error_message: Optional[str]
    auth_bytes: bytes
    session_lifetime_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.SASL_AUTHENTICATE

    def __init__(
        self, error_code: ErrorCode, error_message: Optional[str], auth_bytes: bytes, session_lifetime_ms: int
    ):
        """
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param error_message: The error message, or null if there was no error.
        :type error_message: Optional[str]
        :param auth_bytes: The SASL authentication bytes from the server, as defined by the SASL mechanism.
        :type auth_bytes: bytes
        :param session_lifetime_ms: The SASL authentication bytes from the server, as defined by the SASL mechanism.
        :type session_lifetime_ms: int
        """
        self.error_code = error_code
        self.error_message = error_message
        self.auth_bytes = auth_bytes
        self.session_lifetime_ms = session_lifetime_ms
