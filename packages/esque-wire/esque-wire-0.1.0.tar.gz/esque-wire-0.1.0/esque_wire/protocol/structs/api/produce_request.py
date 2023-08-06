from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Data:

    partition: int
    record_set: Optional[bytes]

    def __init__(self, partition: int, record_set: Optional[bytes]):
        """
        :param partition: Topic partition id
        :type partition: int
        :param record_set: None
        :type record_set: Optional[bytes]
        """
        self.partition = partition
        self.record_set = record_set


class TopicData:

    topic: str
    data: List[Data]

    def __init__(self, topic: str, data: List[Data]):
        """
        :param topic: Name of topic
        :type topic: str
        :param data: None
        :type data: List[Data]
        """
        self.topic = topic
        self.data = data


class ProduceRequestData(RequestData):

    transactional_id: Optional[str]
    acks: int
    timeout: int
    topic_data: List[TopicData]
    api_key: ClassVar[ApiKey] = ApiKey.PRODUCE

    def __init__(self, transactional_id: Optional[str], acks: int, timeout: int, topic_data: List[TopicData]):
        """
        :param transactional_id: The transactional id or null if the producer is not transactional
        :type transactional_id: Optional[str]
        :param acks: The number of acknowledgments the producer requires the leader to have received before considering
                     a request complete. Allowed values: 0 for no acknowledgments, 1 for only the leader and -1 for the
                     full ISR.
        :type acks: int
        :param timeout: The time to await a response in ms.
        :type timeout: int
        :param topic_data: None
        :type topic_data: List[TopicData]
        """
        self.transactional_id = transactional_id
        self.acks = acks
        self.timeout = timeout
        self.topic_data = topic_data
