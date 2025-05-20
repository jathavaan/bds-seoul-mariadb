import json
from logging import Logger

from confluent_kafka import Consumer

from src import Config
from src.entrypoints.base import ConsumerBase


class MapreduceResultConsumer(ConsumerBase[dict[str, tuple[float, float]] | None]):
    __consumer: Consumer
    __logger: Logger

    def __init__(self):
        topics = [Config.KAFKA_RESULT_TOPIC.value]
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        })

        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> tuple[bool, dict[str, tuple[float, float]]] | None:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return None

        if message.error():
            self.__logger.error(message.error())
            return None

        game_id = message.key()
        mapreduce_result: dict[str, tuple[float, float]] = json.loads(message.value().decode("utf-8"))

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down map reduce result consumer")
