import json
from logging import Logger
from typing import Sequence

from confluent_kafka import Consumer

from src import Config
from src.application.services.game_service import GameRepositoryService
from src.application.services.recommendation_service import RecommendationDto, RecommendationRepositoryService, \
    FinalResultDto
from src.domain.entities import Recommendation
from src.entrypoints.base import ConsumerBase


class MapreduceResultConsumer(ConsumerBase[tuple[bool, FinalResultDto | None]]):
    __consumer: Consumer
    __logger: Logger
    __game_repository_service: GameRepositoryService
    __recommendation_repository_service: RecommendationRepositoryService

    def __init__(
            self,
            logger: Logger,
            game_repository_service: GameRepositoryService,
            recommendation_repository_service: RecommendationRepositoryService
    ):
        self.__logger = logger
        self.__game_repository_service = game_repository_service
        self.__recommendation_repository_service = recommendation_repository_service
        topics = [Config.KAFKA_MR_RESULT_TOPIC.value]
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "max.poll.interval.ms": Config.KAFKA_MAX_POLL_TIMEOUT.value
        })

        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> tuple[bool, FinalResultDto | None]:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False, None

        if message.error():
            self.__logger.error(message.error())
            return False, None

        self.__logger.info("Result from MapReduce received... Saving results in database")
        steam_game_id = int(message.key().decode('utf-8')) if message.key() else None
        if not steam_game_id:
            self.__logger.error("Steam game ID not provided")
            return False, None

        mapreduce_result = FinalResultDto(**json.loads(message.value().decode("utf-8")))
        game = self.__game_repository_service.find_game_by_steam_game_id(steam_game_id)

        if not game:
            self.__logger.error(
                f"Trying to search for a Steam Game ID [{steam_game_id}] that have not been added to the database yet. The data is broken and cannot be added "
            )
            return False, None

        self.__recommendation_repository_service.upsert_result(
            game_id=game.id,
            recommendation_dtos=mapreduce_result.recommendations
        )

        recommendations = self.__recommendation_repository_service.get_recommendations_by_game_id(game_id=game.id)
        recommendation_dtos = MapreduceResultConsumer.__convert_recommendation_entities_to_dtos(recommendations)

        final_result_dto = FinalResultDto(
            game_id=game.steam_game_id,
            correlation_id=mapreduce_result.correlation_id,
            recommendations=recommendation_dtos
        )

        return True, final_result_dto

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down map reduce result consumer")

    @staticmethod
    def __convert_recommendation_entities_to_dtos(recommendations: Sequence[Recommendation]) -> list[
        RecommendationDto
    ]:
        return [
            RecommendationDto(
                recommendation.time_interval,
                float(recommendation.sum_recommended),
                float(recommendation.sum_not_recommended)
            )
            for recommendation in recommendations
        ]
