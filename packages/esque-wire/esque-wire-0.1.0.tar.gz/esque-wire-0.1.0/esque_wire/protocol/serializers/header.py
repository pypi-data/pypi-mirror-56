from ..structs.header import RequestHeader, ResponseHeader
from .constants import apiKeySerializer
from .generic import ClassSerializer, Schema
from .primitive import int16Serializer, int32Serializer, nullableStringSerializer

requestHeaderSchema: Schema = [
    ("api_key", apiKeySerializer),
    ("api_version", int16Serializer),
    ("correlation_id", int32Serializer),
    ("client_id", nullableStringSerializer),
]

requestHeaderSerializer = ClassSerializer(RequestHeader, requestHeaderSchema)

responseHeaderSchema: Schema = [("correlation_id", int32Serializer)]

responseHeaderSerializer = ClassSerializer(ResponseHeader, responseHeaderSchema)
