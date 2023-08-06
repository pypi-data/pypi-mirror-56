from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class AddOffsetsToTxnRequestData(RequestData):

    transactional_id: str
    producer_id: int
    producer_epoch: int
    group_id: str
    api_key: ClassVar[ApiKey] = ApiKey.ADD_OFFSETS_TO_TXN

    def __init__(self, transactional_id: str, producer_id: int, producer_epoch: int, group_id: str):
        """
        :param transactional_id: The transactional id corresponding to the transaction.
        :type transactional_id: str
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param producer_epoch: Current epoch associated with the producer id.
        :type producer_epoch: int
        :param group_id: The unique group identifier
        :type group_id: str
        """
        self.transactional_id = transactional_id
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
        self.group_id = group_id
