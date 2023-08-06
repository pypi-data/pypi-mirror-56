from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class ControlledShutdownRequestData(RequestData):

    broker_id: int
    broker_epoch: int
    api_key: ClassVar[ApiKey] = ApiKey.CONTROLLED_SHUTDOWN

    def __init__(self, broker_id: int, broker_epoch: int):
        """
        :param broker_id: The id of the broker for which controlled shutdown has been requested.
        :type broker_id: int
        :param broker_epoch: The broker epoch.
        :type broker_epoch: int
        """
        self.broker_id = broker_id
        self.broker_epoch = broker_epoch
