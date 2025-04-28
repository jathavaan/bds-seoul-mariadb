import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_GROUP_ID = "mariadb_consumer_group"
    KAFKA_TOPICS = ["game_topic"]

    LOGGER_WIDTH_OFFSET = 75
