import json
import logging

from confluent_kafka import Consumer

from src import Config
from src.application.services.game_service import GameRepositoryService, LastScrapedDateResponseDto, \
    LastScrapedDateRequestDto
from src.entrypoints.base import ConsumerBase


class LastScrapedDateConsumer(ConsumerBase[LastScrapedDateResponseDto]):
    __logger: logging.Logger
    __consumer: Consumer
    __game_repository_service: GameRepositoryService

    def __init__(self, logger: logging.Logger, game_repository_service: GameRepositoryService):
        self.__logger = logger
        self.__game_repository_service = game_repository_service

        topics = [Config.KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC.value]
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

    def consume(self) -> tuple[bool, LastScrapedDateResponseDto | None]:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False, None

        if message.error():
            self.__logger.error(message.error())
            return False, None

        request = LastScrapedDateRequestDto(**json.loads(message.value().decode("utf-8")))
        self.__logger.info(f"Request last scraped date for Steam game ID {request.game_id} received")
        game = self.__game_repository_service.find_game_by_steam_game_id(request.game_id)

        if not game:
            self.__logger.info(f"No game found for Steam game ID {request.game_id}")
            self.__game_repository_service.add_game(steam_game_id=request.game_id)
            response = LastScrapedDateResponseDto(
                steam_game_id=request.game_id,
                last_scraped_date=None,
                correlation_id=request.correlation_id
            )

            return True, response

        response = LastScrapedDateResponseDto(
            steam_game_id=game.steam_game_id,
            last_scraped_date=game.last_scraped_timestamp,
            correlation_id=request.correlation_id
        )

        return True, response

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Closed Last Scraped Date Consumer")
