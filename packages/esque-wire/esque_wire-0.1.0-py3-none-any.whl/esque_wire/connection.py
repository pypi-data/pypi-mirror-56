import itertools as it
import queue
import socket
import warnings
from typing import BinaryIO, Dict, List, Tuple

from ._base_connection import BaseBrokerConnection
from .protocol.constants import ApiKey
from .protocol.request import Request, Response
from .protocol.serializers import SUPPORTED_API_VERSIONS, int32Serializer
from .protocol.structs.api import ApiVersionsRequestData
from .protocol.structs.api.api_versions_response import ApiVersion
from .protocol.structs.base import RequestData


class ApiNotSupportedWarning(UserWarning):
    pass


class BrokerConnection(BaseBrokerConnection):
    def __init__(self, host: str, client_id: str):
        host, port = host.split(":")
        self.kafka_io = KafkaIO.from_address((host, int(port)))
        self.client_id = client_id
        self._correlation_id_counter = it.count()
        self.api_versions: Dict[ApiKey, int] = {ApiKey.API_VERSIONS: 1}
        self._query_api_versions()

    def _query_api_versions(self) -> None:
        api_call = self.send(ApiVersionsRequestData())

        all_server_supported_versions = {
            ApiKey(support_range.api_key): support_range for support_range in api_call.response_data.api_versions
        }
        server_api_keys = set(all_server_supported_versions)
        client_api_keys = set(SUPPORTED_API_VERSIONS)
        for api_key in server_api_keys | client_api_keys:
            client_supported_version = SUPPORTED_API_VERSIONS.get(api_key, ApiVersion(api_key, -2, -1))
            server_supported_version = all_server_supported_versions.get(api_key, ApiVersion(api_key, -4, -3))
            effective_version = min(client_supported_version.max_version, server_supported_version.max_version)

            # TODO messages say something like server only supports api ... up to version -4
            #  better say server doesn't support api ... PERIOD
            # I'd like to do warings/exceptions during runtime once a feature is actually needed. This makes sure the
            # client can be used for everything where the api versions match and/or are high enough.
            # In the high level part, I imagine function annotations like @requires(ApiKey.LIST_OFFSETS, 2) if a
            # function requires the server to support api LIST_OFFSETS of at least version 2
            if effective_version < client_supported_version.min_version:
                if server_supported_version.max_version == -3:
                    warnings.warn(
                        ApiNotSupportedWarning(
                            f"Client supports API {api_key.name} up to version {client_supported_version.max_version}, "
                            + f"but server does not support the API at all. You cannot use this API."
                        )
                    )
                else:
                    warnings.warn(
                        ApiNotSupportedWarning(
                            f"Server only supports API {api_key.name} up to version"
                            f"{server_supported_version.max_version}, but client needs at least "
                            f"{client_supported_version.min_version}. You cannot use this API."
                        )
                    )
            if effective_version < server_supported_version.min_version:
                if client_supported_version.max_version == -1:
                    warnings.warn(
                        ApiNotSupportedWarning(
                            f"Server supports api {api_key.name} up to version {server_supported_version.max_version}, "
                            + f"but client does not support the API at all. You cannot use this API."
                        )
                    )
                else:
                    warnings.warn(
                        ApiNotSupportedWarning(
                            f"Client only supports API {api_key.name} up to version"
                            f"{client_supported_version.max_version}, but server needs at least "
                            f"{server_supported_version.min_version}. You cannot use this API."
                        )
                    )
            self.api_versions[api_key] = effective_version

    def _send(self, request_data: RequestData) -> Response:
        return self.send_many([request_data])[0]

    def send_many(self, request_data_to_send: List[RequestData]) -> List[Response]:
        requests_to_send = [self._request_from_data(data) for data in request_data_to_send]

        responses_received: List[Response] = []

        responses_expected = len(request_data_to_send)
        if responses_expected == 0:
            return []

        while len(responses_received) < responses_expected:
            self._try_send_and_pop_from(requests_to_send)
            self._try_receive_and_append_to(responses_received)
        return responses_received

    def _try_send_and_pop_from(self, requests_to_send: List[Request]) -> None:
        if len(requests_to_send) == 0:
            return
        try:
            self.kafka_io.send(requests_to_send[0])
            del requests_to_send[0]

            if len(requests_to_send) == 0:  # we're now empty, flush all messages
                self.kafka_io.flush()
        except queue.Full:  # make sure we flush so some messages can be read to make place for new ones
            self.kafka_io.flush()

    def _try_receive_and_append_to(self, received_requests: List[Response]) -> None:
        try:
            received_requests.append(self.kafka_io.receive())
        except queue.Empty:
            pass

    def _request_from_data(self, request_data: RequestData) -> Request:
        api_key = request_data.api_key
        api_version = self.api_versions[api_key]
        return Request.from_request_data(request_data, api_version, next(self._correlation_id_counter), self.client_id)

    def close(self):
        self.kafka_io.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()


class KafkaIO:
    def __init__(self, in_stream: BinaryIO, out_stream: BinaryIO):
        self._in_flight: "queue.Queue[Request]" = queue.Queue(maxsize=10)  # TODO make this configurable
        self._in_stream: BinaryIO = in_stream
        self._out_stream: BinaryIO = out_stream

    def send(self, api_call: Request) -> None:
        data = api_call.encode_request()
        self._send_req_data(api_call, data)

    def _send_req_data(self, api_call: Request, data: bytes) -> None:
        self._in_flight.put(api_call, block=False)
        self._out_stream.write(int32Serializer.encode(len(data)))
        self._out_stream.write(data)

    def receive(self) -> Response:
        request, data = self._receive_req_data()
        response: Response = request.decode_response(data)
        self._in_flight.task_done()
        return response

    def _receive_req_data(self) -> Tuple[Request, bytes]:
        request = self._in_flight.get(block=False)
        len_ = int32Serializer.read(self._in_stream)
        data = self._in_stream.read(len_)
        return request, data

    def flush(self):
        self._out_stream.flush()

    @classmethod
    def from_socket(cls, io_socket: socket.SocketType) -> "KafkaIO":
        in_stream = io_socket.makefile(mode="rb", buffering=4096)
        out_stream = io_socket.makefile(mode="wb", buffering=4096)
        return cls(in_stream, out_stream)

    @classmethod
    def from_address(cls, address: Tuple[str, int]) -> "KafkaIO":
        io_socket = socket.create_connection(address)
        return cls.from_socket(io_socket)

    def close(self):
        self._in_stream.close()
        self._out_stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
