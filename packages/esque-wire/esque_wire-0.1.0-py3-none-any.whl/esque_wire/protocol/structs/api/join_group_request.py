from typing import ClassVar, List, Optional

from ...constants import ApiKey
from ..base import RequestData


class Protocol:

    name: str
    metadata: bytes

    def __init__(self, name: str, metadata: bytes):
        """
        :param name: The protocol name.
        :type name: str
        :param metadata: The protocol metadata.
        :type metadata: bytes
        """
        self.name = name
        self.metadata = metadata


class JoinGroupRequestData(RequestData):

    group_id: str
    session_timeout_ms: int
    rebalance_timeout_ms: int
    member_id: str
    group_instance_id: Optional[str]
    protocol_type: str
    protocols: List[Protocol]
    api_key: ClassVar[ApiKey] = ApiKey.JOIN_GROUP

    def __init__(
        self,
        group_id: str,
        session_timeout_ms: int,
        rebalance_timeout_ms: int,
        member_id: str,
        group_instance_id: Optional[str],
        protocol_type: str,
        protocols: List[Protocol],
    ):
        """
        :param group_id: The group identifier.
        :type group_id: str
        :param session_timeout_ms: The coordinator considers the consumer dead if it receives no heartbeat after this
                                   timeout in milliseconds.
        :type session_timeout_ms: int
        :param rebalance_timeout_ms: The maximum time in milliseconds that the coordinator will wait for each member to
                                     rejoin when rebalancing the group.
        :type rebalance_timeout_ms: int
        :param member_id: The member id assigned by the group coordinator.
        :type member_id: str
        :param group_instance_id: The unique identifier of the consumer instance provided by end user.
        :type group_instance_id: Optional[str]
        :param protocol_type: The unique name the for class of protocols implemented by the group we want to join.
        :type protocol_type: str
        :param protocols: The list of protocols that the member supports.
        :type protocols: List[Protocol]
        """
        self.group_id = group_id
        self.session_timeout_ms = session_timeout_ms
        self.rebalance_timeout_ms = rebalance_timeout_ms
        self.member_id = member_id
        self.group_instance_id = group_instance_id
        self.protocol_type = protocol_type
        self.protocols = protocols
