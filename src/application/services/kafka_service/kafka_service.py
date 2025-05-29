import logging

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, KafkaException, KafkaError

from src import Config


class KafkaService:
    __logger: logging.Logger
    __admin_client: AdminClient

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__admin_client = AdminClient({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

        self.__logger.info("KafkaService initialized and attempting to create topics")

        topics = [
            NewTopic(topic=Config.KAFKA_REVIEW_TOPIC.value, num_partitions=1, replication_factor=1),
            NewTopic(topic=Config.KAFKA_MR_RESULT_TOPIC.value, num_partitions=1, replication_factor=1),
            NewTopic(topic=Config.KAFKA_FINAL_RESULT_TOPIC.value, num_partitions=1, replication_factor=1),
            NewTopic(topic=Config.KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC.value, num_partitions=1, replication_factor=1),
            NewTopic(topic=Config.KAFKA_LAST_SCRAPED_DATE_RES_TOPIC.value, num_partitions=1, replication_factor=1),
            NewTopic(topic=Config.KAFKA_PROCESS_STATUS_TOPIC.value, num_partitions=1, replication_factor=1),
        ]

        futures = self.__admin_client.create_topics(new_topics=topics)
        for topic, future in futures.items():
            try:
                future.result()
                self.__logger.info(f"Created topic {topic}")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    self.__logger.info(f"Topic '{topic}' already exists.")
                else:
                    self.__logger.error(f"Failed to create topic '{topic}': {e}")
            except Exception as e:
                self.__logger.error(f"Failed to crate topic {topic}: {e}")
