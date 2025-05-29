import logging
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_STARTUP_WAIT_TIME = 10

    KAFKA_BOOTSTRAP_SERVERS = f"{os.getenv('KAFKA_BOOTSTRAP_SERVERS')}:9092"
    KAFKA_GROUP_ID = "seoul"
    KAFKA_POLL_TIMEOUT = 1.0

    KAFKA_REVIEW_TOPIC = "reviews"
    KAFKA_MR_RESULT_TOPIC = "mapreduce_results"
    KAFKA_FINAL_RESULT_TOPIC = "final_results"
    KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC = "last_scraped_date_requests"
    KAFKA_LAST_SCRAPED_DATE_RES_TOPIC = "last_scraped_date_responses"
    KAFKA_PROCESS_STATUS_TOPIC = "process_status"

    LOGGING_LEVEL = logging.INFO
    LOGGER_WIDTH_OFFSET = 90
    SEQ_URL = f"http://{os.getenv('SEQ_SERVER')}:{os.getenv('SEQ_PORT')}"
    SEQ_LOG_BATCH_SIZE = 1
