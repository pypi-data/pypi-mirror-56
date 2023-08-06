from typing import ClassVar

from ...constants import ApiKey
from ..base import RequestData


class EndTxnRequestData(RequestData):

    transactional_id: str
    producer_id: int
    producer_epoch: int
    transaction_result: bool
    api_key: ClassVar[ApiKey] = ApiKey.END_TXN

    def __init__(self, transactional_id: str, producer_id: int, producer_epoch: int, transaction_result: bool):
        """
        :param transactional_id: The transactional id corresponding to the transaction.
        :type transactional_id: str
        :param producer_id: Current producer id in use by the transactional id.
        :type producer_id: int
        :param producer_epoch: Current epoch associated with the producer id.
        :type producer_epoch: int
        :param transaction_result: The result of the transaction (0 = ABORT, 1 = COMMIT)
        :type transaction_result: bool
        """
        self.transactional_id = transactional_id
        self.producer_id = producer_id
        self.producer_epoch = producer_epoch
        self.transaction_result = transaction_result
