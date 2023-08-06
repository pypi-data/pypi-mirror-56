from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class SaslHandshakeRequestData(RequestData):

    mechanism: str
    api_key: ClassVar[ApiKey] = ApiKey.SASL_HANDSHAKE

    def __init__(self, mechanism: str):
        """
        :param mechanism: The SASL mechanism chosen by the client.
        :type mechanism: str
        """
        self.mechanism = mechanism
