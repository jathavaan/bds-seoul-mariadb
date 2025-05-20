from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped

from src.domain.base import EntityBase

if TYPE_CHECKING:
    from src.domain.entities.playtime_recommendation import PlaytimeRecommendation


class Game(EntityBase):
    __tablename__ = "games"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_timestamp: Mapped[datetime] = Column(DateTime, nullable=False)
    last_scraped_timestamp: Mapped[datetime] = Column(DateTime, nullable=False)
    steam_game_id: Mapped[int] = Column(Integer, nullable=False)

    playtime_recommendations: Mapped[list["PlaytimeRecommendation"]] = relationship(
        "PlaytimeRecommendation",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    def __init__(self, steam_game_id: int):
        super().__init__()
        self.steam_game_id = steam_game_id
        current_timestamp = datetime.now()
        self.created_timestamp = current_timestamp
        self.last_scraped_timestamp = current_timestamp
