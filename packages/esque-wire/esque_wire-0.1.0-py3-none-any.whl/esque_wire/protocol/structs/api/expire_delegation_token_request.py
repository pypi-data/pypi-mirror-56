from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class ExpireDelegationTokenRequestData(RequestData):

    hmac: bytes
    expiry_time_period: int
    api_key: ClassVar[ApiKey] = ApiKey.EXPIRE_DELEGATION_TOKEN

    def __init__(self, hmac: bytes, expiry_time_period: int):
        """
        :param hmac: HMAC of the delegation token to be expired.
        :type hmac: bytes
        :param expiry_time_period: expiry time period in milli seconds.
        :type expiry_time_period: int
        """
        self.hmac = hmac
        self.expiry_time_period = expiry_time_period
