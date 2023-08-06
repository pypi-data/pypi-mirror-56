from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class Partition:

    topic: str
    partition_ids: List[int]

    def __init__(self, topic: str, partition_ids: List[int]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_ids: The partition ids of a topic
        :type partition_ids: List[int]
        """
        self.topic = topic
        self.partition_ids = partition_ids


class StopReplicaRequestData(RequestData):

    controller_id: int
    controller_epoch: int
    broker_epoch: int
    delete_partitions: bool
    partitions: List[Partition]
    api_key: ClassVar[ApiKey] = ApiKey.STOP_REPLICA

    def __init__(
        self,
        controller_id: int,
        controller_epoch: int,
        broker_epoch: int,
        delete_partitions: bool,
        partitions: List[Partition],
    ):
        """
        :param controller_id: The controller id
        :type controller_id: int
        :param controller_epoch: The controller epoch
        :type controller_epoch: int
        :param broker_epoch: The broker epoch
        :type broker_epoch: int
        :param delete_partitions: Boolean which indicates if replica's partitions must be deleted.
        :type delete_partitions: bool
        :param partitions: The partitions
        :type partitions: List[Partition]
        """
        self.controller_id = controller_id
        self.controller_epoch = controller_epoch
        self.broker_epoch = broker_epoch
        self.delete_partitions = delete_partitions
        self.partitions = partitions
