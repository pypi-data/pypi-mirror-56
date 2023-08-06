from typing import ClassVar, Optional

from ...constants import ApiKey
from ..base import RequestData


class InitProducerIdRequestData(RequestData):

    transactional_id: Optional[str]
    transaction_timeout_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.INIT_PRODUCER_ID

    def __init__(self, transactional_id: Optional[str], transaction_timeout_ms: int):
        """
        :param transactional_id: The transactional id, or null if the producer is not transactional.
        :type transactional_id: Optional[str]
        :param transaction_timeout_ms: The time in ms to wait for before aborting idle transactions sent by this
                                       producer. This is only relevant if a TransactionalId has been defined.
        :type transaction_timeout_ms: int
        """
        self.transactional_id = transactional_id
        self.transaction_timeout_ms = transaction_timeout_ms
