from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class EndPoint:

    port: int
    host: str
    listener_name: str
    security_protocol_type: int

    def __init__(self, port: int, host: str, listener_name: str, security_protocol_type: int):
        """
        :param port: The port on which the broker accepts requests.
        :type port: int
        :param host: The hostname of the broker.
        :type host: str
        :param listener_name: The listener name.
        :type listener_name: str
        :param security_protocol_type: The security protocol type.
        :type security_protocol_type: int
        """
        self.port = port
        self.host = host
        self.listener_name = listener_name
        self.security_protocol_type = security_protocol_type


class LiveBroker:

    id: int
    end_points: List[EndPoint]
    rack: Optional[str]

    def __init__(self, id: int, end_points: List[EndPoint], rack: Optional[str]):
        """
        :param id: The broker id
        :type id: int
        :param end_points: The endpoints
        :type end_points: List[EndPoint]
        :param rack: The rack
        :type rack: Optional[str]
        """
        self.id = id
        self.end_points = end_points
        self.rack = rack


class PartitionState:

    partition: int
    controller_epoch: int
    leader: int
    leader_epoch: int
    isr: List[int]
    zk_version: int
    replicas: List[int]
    offline_replicas: List[int]

    def __init__(
        self,
        partition: int,
        controller_epoch: int,
        leader: int,
        leader_epoch: int,
        isr: List[int],
        zk_version: int,
        replicas: List[int],
        offline_replicas: List[int],
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
        :param offline_replicas: The offline replica ids
        :type offline_replicas: List[int]
        """
        self.partition = partition
        self.controller_epoch = controller_epoch
        self.leader = leader
        self.leader_epoch = leader_epoch
        self.isr = isr
        self.zk_version = zk_version
        self.replicas = replicas
        self.offline_replicas = offline_replicas


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


class UpdateMetadataRequestData(RequestData):

    controller_id: int
    controller_epoch: int
    broker_epoch: int
    topic_states: List[TopicState]
    live_brokers: List[LiveBroker]
    api_key: ClassVar[ApiKey] = ApiKey.UPDATE_METADATA

    def __init__(
        self,
        controller_id: int,
        controller_epoch: int,
        broker_epoch: int,
        topic_states: List[TopicState],
        live_brokers: List[LiveBroker],
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
        :param live_brokers: Live broekrs
        :type live_brokers: List[LiveBroker]
        """
        self.controller_id = controller_id
        self.controller_epoch = controller_epoch
        self.broker_epoch = broker_epoch
        self.topic_states = topic_states
        self.live_brokers = live_brokers
