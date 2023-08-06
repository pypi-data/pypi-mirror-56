from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


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


class CreateDelegationTokenRequestData(RequestData):

    renewers: List[Renewer]
    max_life_time: int
    api_key: ClassVar[ApiKey] = ApiKey.CREATE_DELEGATION_TOKEN

    def __init__(self, renewers: List[Renewer], max_life_time: int):
        """
        :param renewers: An array of token renewers. Renewer is an Kafka PrincipalType and name string, who is allowed
                         to renew this token before the max lifetime expires.
        :type renewers: List[Renewer]
        :param max_life_time: Max lifetime period for token in milli seconds. if value is -1, then max lifetime  will
                              default to a server side config value.
        :type max_life_time: int
        """
        self.renewers = renewers
        self.max_life_time = max_life_time
