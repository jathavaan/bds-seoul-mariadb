from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from src.domain.base import EntityBase


class Game(EntityBase):
    __tablename__ = "games"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_timestamp: datetime = Column(DateTime, nullable=False)
    last_scraped_timestamp: datetime = Column(DateTime, nullable=False)
    steam_game_id: int = Column(Integer, nullable=False)

    def __init__(self, steam_game_id: int):
        self.steam_game_id = steam_game_id
        current_timestamp = datetime.now()
        self.created_timestamp = current_timestamp
        self.last_scraped_timestamp = current_timestamp
