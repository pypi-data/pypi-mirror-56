from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


class LiveLeader:

    id: int
    host: str
    port: int

    def __init__(self, id: int, host: str, port: int):
        """
        :param id: The broker id
        :type id: int
        :param host: The hostname of the broker.
        :type host: str
        :param port: The port on which the broker accepts requests.
        :type port: int
        """
        self.id = id
        self.host = host
        self.port = port


class PartitionState:

    partition: int
    controller_epoch: int
    leader: int
    leader_epoch: int
    isr: List[int]
    zk_version: int
    replicas: List[int]
    is_new: bool

    def __init__(
        self,
        partition: int,
        controller_epoch: int,
        leader: int,
        leader_epoch: int,
        isr: List[int],
        zk_version: int,
        replicas: List[int],
        is_new: bool,
    ):
        """
        :param partition: Topic partition id
        :type partition: int
        :param controller_epoch: The controller epoch
        :type controller_epoch: int
        :param leader: The broker id for the leader.
        :type leader: int
        :param leader_epoch: The leader epoch.
        :type leader_epoch: int
        :param isr: The in sync replica ids.
        :type isr: List[int]
        :param zk_version: The ZK version.
        :type zk_version: int
        :param replicas: The replica ids.
        :type replicas: List[int]
        :param is_new: Whether the replica should have existed on the broker or not
        :type is_new: bool
        """
        self.partition = partition
        self.controller_epoch = controller_epoch
        self.leader = leader
        self.leader_epoch = leader_epoch
        self.isr = isr
        self.zk_version = zk_version
        self.replicas = replicas
        self.is_new = is_new


class TopicState:

    topic: str
    partition_states: List[PartitionState]

    def __init__(self, topic: str, partition_states: List[PartitionState]):
        """
        :param topic: Name of topic
        :type topic: str
        :param partition_states: Partition states
        :type partition_states: List[PartitionState]
        """
        self.topic = topic
        self.partition_states = partition_states


class LeaderAndIsrRequestData(RequestData):

    controller_id: int
    controller_epoch: int
    broker_epoch: int
    topic_states: List[TopicState]
    live_leaders: List[LiveLeader]
    api_key: ClassVar[ApiKey] = ApiKey.LEADER_AND_ISR

    def __init__(
        self,
        controller_id: int,
        controller_epoch: int,
        broker_epoch: int,
        topic_states: List[TopicState],
        live_leaders: List[LiveLeader],
    ):
        """
        :param controller_id: The controller id
        :type controller_id: int
        :param controller_epoch: The controller epoch
        :type controller_epoch: int
        :param broker_epoch: The broker epoch
        :type broker_epoch: int
        :param topic_states: Topic states
        :type topic_states: List[TopicState]
        :param live_leaders: Live leaders
        :type live_leaders: List[LiveLeader]
        """
        self.controller_id = controller_id
        self.controller_epoch = controller_epoch
        self.broker_epoch = broker_epoch
        self.topic_states = topic_states
        self.live_leaders = live_leaders
