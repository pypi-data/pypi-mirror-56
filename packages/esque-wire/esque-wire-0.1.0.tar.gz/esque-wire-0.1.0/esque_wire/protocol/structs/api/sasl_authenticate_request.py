from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class SaslAuthenticateRequestData(RequestData):

    auth_bytes: bytes
    api_key: ClassVar[ApiKey] = ApiKey.SASL_AUTHENTICATE

    def __init__(self, auth_bytes: bytes):
        """
        :param auth_bytes: The SASL authentication bytes from the client, as defined by the SASL mechanism.
        :type auth_bytes: bytes
        """
        self.auth_bytes = auth_bytes
