from typing import Optional

from ..constants import ApiKey


class RequestHeader:
    api_key: ApiKey
    api_version: int  # INT16
    correlation_id: int  # INT32
    client_id: Optional[str]

    def __init__(self, api_key: ApiKey, api_version: int, correlation_id: int, client_id: Optional[str]):
        self.api_key = api_key
        self.api_version = api_version
        self.correlation_id = correlation_id
        self.client_id = client_id


class ResponseHeader:
    correlation_id: int  # INT32

    def __init__(self, correlation_id: int):
        self.correlation_id = correlation_id
