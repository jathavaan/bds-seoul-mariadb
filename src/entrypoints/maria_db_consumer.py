import logging

from confluent_kafka import Consumer

from src import Config
from src.application import Container


class MariaDbConsumer:
    __consumer: Consumer
    __logger: logging.Logger

    def __init__(self):
        container = Container()
        self.__logger = container.logger()
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        })

        topics = [Config.KAFKA_REVIEW_TOPIC.value]
        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> None:
        while True:
            message = self.__consumer.poll(1.0)

            if not message:
                continue

            if message.error():
                self.__logger.error(message.error())
                continue

            self.__logger.info(
                f"Received message on topic '{message.topic()}' [partition {message.partition()}] "
                f"offset {message.offset()}: key={message.key()} value={message.value().decode('utf-8')}"
            )

    def close(self) -> None:
        self.__logger.info("Shutting down MariaDB consumer")
        self.__consumer.close()
