from typing import TypeVar, Generic

T = TypeVar("T")


class KafkaBase:
    def close(self) -> None:
        raise NotImplementedError("Close method not implemented")


class ConsumerBase(Generic[T], KafkaBase):
    def consume(self) -> tuple[bool, T]:
        raise NotImplementedError("Consume method not implemented")


class ProducerBase(Generic[T], KafkaBase):
    def produce(self, producer_content: T) -> None:
        raise NotImplementedError("Produce method not implemented")
