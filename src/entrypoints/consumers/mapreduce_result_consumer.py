import json
from logging import Logger

from confluent_kafka import Consumer

from src import Config
from src.application.services.game_service import GameRepositoryService
from src.application.services.recommendation_service import RecommendationDto, RecommendationRepositoryService
from src.entrypoints.base import ConsumerBase


class MapreduceResultConsumer(ConsumerBase[bool]):
    __consumer: Consumer
    __logger: Logger
    __game_repository_service: GameRepositoryService
    __playtime_recommendation_repository_service: RecommendationRepositoryService

    def __init__(
            self,
            logger: Logger,
            game_repository_service: GameRepositoryService,
            playtime_recommendation_repository_service: RecommendationRepositoryService
    ):
        self.__logger = logger
        self.__game_repository_service = game_repository_service
        self.__playtime_recommendation_repository_service = playtime_recommendation_repository_service
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

    def consume(self) -> bool:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False

        if message.error():
            self.__logger.error(message.error())
            return False

        self.__logger.info("Result from MapReduce received... Saving results in database")
        steam_game_id = int(message.key().decode('utf-8')) if message.key() else None
        if not steam_game_id:
            self.__logger.error("Steam game ID not provided")
            return False

        mapreduce_result: dict[str, tuple[float, float]] = json.loads(message.value().decode("utf-8"))

        playtime_recommendation_dtos: list[RecommendationDto] = []

        for key, values in mapreduce_result.items():
            sum_recommended, sum_not_recommended = values
            dto = RecommendationDto(
                time_interval=key,
                sum_recommended=sum_recommended,
                sum_not_recommended=sum_not_recommended
            )

            playtime_recommendation_dtos.append(dto)

        game_id = self.__game_repository_service.find_game_id_by_steam_game_id(steam_game_id)
        if not game_id:
            self.__logger.error(
                f"Trying to search for a Steam Game ID [{steam_game_id}] that have not been added to the database yet. The data is broken and cannot be added "
            )
            return False

        self.__playtime_recommendation_repository_service.upsert_result(
            game_id=game_id,
            recommendation_dtos=playtime_recommendation_dtos
        )

        return True

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shut down map reduce result consumer")
