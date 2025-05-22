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

    def find_game_by_steam_game_id(self, steam_game_id: int) -> Game | None:
        return self.__db_session.scalars(select(Game).where(Game.steam_game_id == steam_game_id)).first()

    def add_game(self, steam_game_id: int) -> None:
        self.__logger.info(f"Adding game with Steam game ID {steam_game_id} to database")
        game = Game(steam_game_id=steam_game_id)
        self.__db_session.add(game)
        self.__db_session.commit()
