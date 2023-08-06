from typing import ClassVar, Optional

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class FindCoordinatorResponseData(ResponseData):

    throttle_time_ms: int
    error_code: ErrorCode
    error_message: Optional[str]
    node_id: int
    host: str
    port: int
    api_key: ClassVar[ApiKey] = ApiKey.FIND_COORDINATOR

    def __init__(
        self,
        throttle_time_ms: int,
        error_code: ErrorCode,
        error_message: Optional[str],
        node_id: int,
        host: str,
        port: int,
    ):
        """
        :param throttle_time_ms: The duration in milliseconds for which the request was throttled due to a quota
                                 violation, or zero if the request did not violate any quota.
        :type throttle_time_ms: int
        :param error_code: The error code, or 0 if there was no error.
        :type error_code: ErrorCode
        :param error_message: The error message, or null if there was no error.
        :type error_message: Optional[str]
        :param node_id: The node id.
        :type node_id: int
        :param host: The host name.
        :type host: str
        :param port: The port.
        :type port: int
        """
        self.throttle_time_ms = throttle_time_ms
        self.error_code = error_code
        self.error_message = error_message
        self.node_id = node_id
        self.host = host
        self.port = port
