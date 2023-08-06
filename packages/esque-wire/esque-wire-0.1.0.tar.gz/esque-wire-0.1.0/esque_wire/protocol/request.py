from io import BytesIO
from typing import BinaryIO, Generic, Optional, Type, TypeVar, cast

from .constants import ApiKey
from .serializers import REQUEST_SERIALIZERS, RESPONSE_SERIALIZERS
from .serializers.base import BaseSerializer
from .serializers.header import requestHeaderSerializer, responseHeaderSerializer
from .structs.base import RequestData, ResponseData
from .structs.header import RequestHeader, ResponseHeader


def get_request_serializer(api_key: ApiKey, api_version: int) -> BaseSerializer[RequestData]:
    return REQUEST_SERIALIZERS[api_key][api_version]


def get_response_serializer(api_key: ApiKey, api_version: int) -> BaseSerializer[ResponseData]:
    return RESPONSE_SERIALIZERS[api_key][api_version]


Req = TypeVar("Req", bound=RequestData)
Res = TypeVar("Res", bound=ResponseData)


class Request(Generic[Req]):
    def __init__(self, request_data: Req, request_header: RequestHeader):
        self.api_version = request_header.api_version
        self.request_data = request_data
        self.request_header = request_header

    def encode_request(self) -> bytes:
        data = requestHeaderSerializer.encode(self.request_header)
        data += self.request_serializer.encode(self.request_data)
        return data

    @property
    def correlation_id(self) -> int:
        return self.request_header.correlation_id

    @property
    def api_key(self) -> ApiKey:
        return self.request_header.api_key

    @property
    def response_serializer(self) -> BaseSerializer[Res]:
        return cast(BaseSerializer[Res], get_response_serializer(self.api_key, self.api_version))

    @property
    def request_serializer(self) -> BaseSerializer[Req]:
        return cast(BaseSerializer[Req], get_request_serializer(self.api_key, self.api_version))

    @classmethod
    def from_request_data(
        cls: "Type[Request[Req]]", request_data: Req, api_version: int, correlation_id: int, client_id: Optional[str]
    ) -> "Request[Req]":
        request_data = request_data
        header = RequestHeader(
            api_key=request_data.api_key, api_version=api_version, correlation_id=correlation_id, client_id=client_id
        )
        return cls(request_data, header)

    def decode_response(self, data: bytes) -> "Response[Req, Res]":
        return self.read_response(BytesIO(data))

    def read_response(self, buffer: BinaryIO) -> "Response[Req, Res]":
        response_header = responseHeaderSerializer.read(buffer)
        if response_header.correlation_id != self.correlation_id:
            # TODO: create proper exception type
            raise RuntimeError("Request and response order got messed up!")
        response_data: Res = self.response_serializer.read(buffer)
        return Response(self, response_data, response_header)


class Response(Generic[Req, Res]):
    request: Request[Req]
    response_data: Res
    response_header: ResponseHeader

    def __init__(self, request: Request[Req], response_data: Res, response_header: ResponseHeader):
        self.request = request
        self.response_data = response_data
        self.response_header = response_header
