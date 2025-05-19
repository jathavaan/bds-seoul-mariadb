from dependency_injector import containers, providers

from src import Config
from src.application.common import Logger


class Container(containers.DeclarativeContainer):
    logger = providers.Factory(Logger.get_logger, name="MariaDB", level=Config.LOGGING_LEVEL.value)
