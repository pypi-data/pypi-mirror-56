from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class RenewDelegationTokenRequestData(RequestData):

    hmac: bytes
    renew_time_period: int
    api_key: ClassVar[ApiKey] = ApiKey.RENEW_DELEGATION_TOKEN

    def __init__(self, hmac: bytes, renew_time_period: int):
        """
        :param hmac: HMAC of the delegation token to be renewed.
        :type hmac: bytes
        :param renew_time_period: Renew time period in milli seconds.
        :type renew_time_period: int
        """
        self.hmac = hmac
        self.renew_time_period = renew_time_period
