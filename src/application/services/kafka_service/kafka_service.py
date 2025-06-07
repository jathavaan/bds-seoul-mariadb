import logging
import time

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic, KafkaException, KafkaError

from src import Config


class KafkaService:
    __logger: logging.Logger
    __admin_client: AdminClient

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__admin_client = AdminClient({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

        self.__logger.info("KafkaService initialized and attempting to clear topics")
        existing_topics = self.__admin_client.list_topics(timeout=10).topics

        topics_to_delete = [
            Config.KAFKA_REVIEW_TOPIC.value,
            Config.KAFKA_MR_RESULT_TOPIC.value,
            Config.KAFKA_FINAL_RESULT_TOPIC.value,
            Config.KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC.value,
            Config.KAFKA_LAST_SCRAPED_DATE_RES_TOPIC.value,
            Config.KAFKA_PROCESS_STATUS_TOPIC.value,
        ]

        topics_to_delete_existing = [t for t in topics_to_delete if t in existing_topics]
        if topics_to_delete_existing:
            delete_result = self.__admin_client.delete_topics(
                topics_to_delete_existing,
                operation_timeout=30,
            )
            for topic, future in delete_result.items():
                try:
                    future.result()
                    self.__logger.info(f"Deleted topic '{topic}'")
                except KafkaException as e:
                    self.__logger.warning(f"Failed to delete topic '{topic}': {e}")
                except Exception as e:
                    self.__logger.error(f"Unexpected error while deleting topic '{topic}': {e}")
        else:
            self.__logger.info("No topics to delete.")

        time.sleep(2)

        self.__logger.info("Attempting to re-create topics")
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
                self.__logger.info(f"Created topic '{topic}'")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                    self.__logger.info(f"Topic '{topic}' already exists.")
                else:
                    self.__logger.error(f"Failed to create topic '{topic}': {e}")
            except Exception as e:
                self.__logger.error(f"Failed to create topic '{topic}': {e}")
