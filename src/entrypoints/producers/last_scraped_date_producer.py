import json
import logging

from confluent_kafka import Producer

from src import Config
from src.application.services.game_service import LastScrapedDateResponseDto
from src.entrypoints.base import ProducerBase


class LastScrapedDateProducer(ProducerBase[LastScrapedDateResponseDto]):
    __logger: logging.Logger
    __producer: Producer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, producer_content: LastScrapedDateResponseDto) -> None:
        self.__producer.produce(
            topic=Config.KAFKA_LAST_SCRAPED_DATE_RES_TOPIC.value,
            value=json.dumps(producer_content.to_dict()),
            callback=self.__delivery_report
        )

        self.__producer.flush()
        self.__logger.info(f"Sent response back to consumer on the topic {Config.KAFKA_LAST_SCRAPED_DATE_RES_TOPIC.value}")

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info("Shut down last scraped date producer")

    def __delivery_report(self, err, msg):
        if err:
            self.__logger.error(f"Delivery failed: {msg}")
        else:
            self.__logger.debug(f"Delivered to {msg.topic()} [partition {msg.partition()}] @ offset {msg.offset()}")
