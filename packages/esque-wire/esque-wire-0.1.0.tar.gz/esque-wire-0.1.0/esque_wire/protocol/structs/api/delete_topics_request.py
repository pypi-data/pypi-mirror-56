from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class DeleteTopicsRequestData(RequestData):

    topic_names: List[str]
    timeout_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.DELETE_TOPICS

    def __init__(self, topic_names: List[str], timeout_ms: int):
        """
        :param topic_names: The names of the topics to delete
        :type topic_names: List[str]
        :param timeout_ms: The length of time in milliseconds to wait for the deletions to complete.
        :type timeout_ms: int
        """
        self.topic_names = topic_names
        self.timeout_ms = timeout_ms
