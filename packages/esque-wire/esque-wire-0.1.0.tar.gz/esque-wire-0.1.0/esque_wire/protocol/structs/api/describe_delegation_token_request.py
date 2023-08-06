from typing import ClassVar, List

from ...constants import ApiKey
from ..base import RequestData


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


class DescribeDelegationTokenRequestData(RequestData):

    owners: List[Owner]
    api_key: ClassVar[ApiKey] = ApiKey.DESCRIBE_DELEGATION_TOKEN

    def __init__(self, owners: List[Owner]):
        """
        :param owners: An array of token owners.
        :type owners: List[Owner]
        """
        self.owners = owners
