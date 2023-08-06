from abc import ABCMeta
from typing import BinaryIO, Generic, TypeVar

T = TypeVar("T")


class BaseSerializer(Generic[T], metaclass=ABCMeta):
    def write(self, buffer: BinaryIO, value: T):
        buffer.write(self.encode(value))

    def encode(self, value: T) -> bytes:
        raise NotImplementedError()

    def read(self, buffer: BinaryIO) -> T:
        raise NotImplementedError()

    @property
    def default(self) -> T:
        raise NotImplementedError()
