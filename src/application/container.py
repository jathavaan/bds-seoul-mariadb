import logging
import time

from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src import Config
from src.application.common import Logger
from src.application.services.game_service import GameRepositoryService
from src.application.services.kafka_service import KafkaService
from src.application.services.recommendation_service import RecommendationRepositoryService

from src.domain.base import EntityBase


def create_db_session(logger: logging.Logger) -> Session:
    logger.info(f"Waiting {Config.SQLALCHEMY_STARTUP_WAIT_TIME.value} seconds while waiting for the database container")
    time.sleep(Config.SQLALCHEMY_STARTUP_WAIT_TIME.value)
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI.value)
    session_maker = sessionmaker(bind=engine)
    EntityBase.metadata.create_all(engine)
    return session_maker()


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger.get_logger, name="MariaDB", level=Config.LOGGING_LEVEL.value)
    db_session = providers.Singleton(create_db_session, logger=logger)

    kafka_service = providers.Singleton(KafkaService, logger=logger)

    game_repository_service = providers.Singleton(
        GameRepositoryService,
        db_session=db_session,
        logger=logger
    )

    recommendation_repository_service = providers.Singleton(
        RecommendationRepositoryService,
        db_session=db_session,
        logger=logger
    )
