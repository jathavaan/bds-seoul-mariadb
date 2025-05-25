import json
import logging

from confluent_kafka.cimpl import Producer

from src import Config
from src.application.services.recommendation_service import RecommendationRepositoryService, FinalResultDto
from src.entrypoints.base import ProducerBase


class FinalResultProducer(ProducerBase[FinalResultDto]):
    __logger: logging.Logger
    __recommendation_repository_service: RecommendationRepositoryService
    __producer: Producer

    def __init__(self, logger: logging.Logger, recommendation_repository_service: RecommendationRepositoryService):
        self.__logger = logger
        self.__recommendation_repository_service = recommendation_repository_service
        self.__producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, producer_content: FinalResultDto) -> None:
        self.__producer.produce(
            topic=Config.KAFKA_FINAL_RESULT_TOPIC.value,
            value=json.dumps(producer_content.to_dict())
        )

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info("Shut down Final result producer")
