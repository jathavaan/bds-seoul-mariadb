import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities import Game


class GameRepositoryService:
    __db_session: Session
    __logger: logging.Logger

    def __init__(self, db_session: Session, logger: logging.Logger):
        self.__db_session = db_session
        self.__logger = logger

    def find_game_id_by_steam_game_id(self, steam_game_id: int) -> int | None:
        return self.__db_session.scalars(select(Game.id).where(Game.steam_game_id == steam_game_id)).first()
