from typing import ClassVar, List

from ...constants import ApiKey, ErrorCode
from ..base import ResponseData


class Renewer:

    principal_type: str
    name: str

    def __init__(self, principal_type: str, name: str):
        """
        :param principal_type: principalType of the Kafka principal
        :type principal_type: str
        :param name: name of the Kafka principal
        :type name: str
        """
        self.principal_type = principal_type
        self.name = name


class Owner:

    principal_type: str
    name: str

    def __init__(self, principal_type: str, name: str):
        """
        :param principal_type: principalType of the Kafka principal
        :type principal_type: str
        :param name: name of the Kafka principal
        :type name: str
        """
        self.principal_type = principal_type
        self.name = name


class TokenDetail:

    owner: Owner
    issue_timestamp: int
    expiry_timestamp: int
    max_timestamp: int
    token_id: str
    hmac: bytes
    renewers: List[Renewer]

    def __init__(
        self,
        owner: Owner,
        issue_timestamp: int,
        expiry_timestamp: int,
        max_timestamp: int,
        token_id: str,
        hmac: bytes,
        renewers: List[Renewer],
    ):
        """
        :param owner: token owner.
        :type owner: Owner
        :param issue_timestamp: timestamp (in msec) when this token was generated.
        :type issue_timestamp: int
        :param expiry_timestamp: timestamp (in msec) at which this token expires.
        :type expiry_timestamp: int
        :param max_timestamp: max life time of this token.
        :type max_timestamp: int
        :param token_id: UUID to ensure uniqueness.
        :type token_id: str
        :param hmac: HMAC of the delegation token to be expired.
        :type hmac: bytes
        :param renewers: An array of token renewers. Renewer is an Kafka PrincipalType and name string, who is allowed
                         to renew this token before the max lifetime expires.
        :type renewers: List[Renewer]
        """
        self.owner = owner
        self.issue_timestamp = issue_timestamp
        self.expiry_timestamp = expiry_timestamp
        self.max_timestamp = max_timestamp
        self.token_id = token_id
        self.hmac = hmac
        self.renewers = renewers


class DescribeDelegationTokenResponseData(ResponseData):

    error_code: ErrorCode
    token_details: List[TokenDetail]
    throttle_time_ms: int
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_DELEGATION_TOKEN

    def __init__(self, error_code: ErrorCode, token_details: List[TokenDetail], throttle_time_ms: int):
        """
        :param error_code: Response error code
        :type error_code: ErrorCode
        :param token_details: None
        :type token_details: List[TokenDetail]
        :param throttle_time_ms: Duration in milliseconds for which the request was throttled due to quota violation
                                 (Zero if the request did not violate any quota)
        :type throttle_time_ms: int
        """
        self.error_code = error_code
        self.token_details = token_details
        self.throttle_time_ms = throttle_time_ms
