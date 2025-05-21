from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src import Config
from src.application.common import Logger
from src.application.services.game_service import GameRepositoryService
from src.application.services.playtime_recommendation_service import PlaytimeRecommendationRepositoryService

from src.domain.base import EntityBase


def create_db_session() -> Session:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI.value)
    session_maker = sessionmaker(bind=engine)
    EntityBase.metadata.create_all(engine)

    return session_maker()


class Container(containers.DeclarativeContainer):
    db_session = providers.Singleton(create_db_session)
    logger = providers.Singleton(Logger.get_logger, name="MariaDB", level=Config.LOGGING_LEVEL.value)

    game_repository_service = providers.Singleton(
        GameRepositoryService,
        db_session=db_session,
        logger=logger
    )

    playtime_recommendation_repository_service = providers.Singleton(
        PlaytimeRecommendationRepositoryService,
        db_session=db_session,
        logger=logger
    )
