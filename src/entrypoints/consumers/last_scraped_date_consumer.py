import logging

from confluent_kafka import Consumer

from src import Config
from src.application.services.game_service import GameRepositoryService
from src.entrypoints.base import ConsumerBase
from src.entrypoints.base.kafka_base import T


class LastScrapedDateConsumer(ConsumerBase):
    __logger: logging.Logger
    __consumer: Consumer
    __game_repository_service: GameRepositoryService

    def __init__(self, logger: logging.Logger, game_repository_service: GameRepositoryService):
        self.__logger = logger
        self.__game_repository_service = game_repository_service

        topics = [Config.KAFKA_LAST_SCRAPED_DATE_REQ.value]
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

    def consume(self) -> tuple[bool, T]:
        pass

    def close(self) -> None:
        pass
