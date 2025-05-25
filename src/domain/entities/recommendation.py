from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from src.domain.base import EntityBase
from src.domain.enums import TimeInterval

if TYPE_CHECKING:
    from src.domain.entities import Game


class Recommendation(EntityBase):
    __tablename__ = "recommendations"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    time_interval: Mapped[TimeInterval] = Column(Enum(TimeInterval, name="time_interval"), nullable=False)
    sum_recommended: Mapped[int] = Column(Integer, nullable=False)
    sum_not_recommended: Mapped[int] = Column(Integer, nullable=False)
    game_id: Mapped[int] = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)

    game: Mapped["Game"] = relationship("Game", back_populates="recommendations")

    def __init__(
            self,
            game_id: int,
            time_interval: TimeInterval,
            sum_recommended: int,
            sum_not_recommended: int
    ) -> None:
        super().__init__()
        self.time_interval = time_interval
        self.sum_recommended = sum_recommended
        self.sum_not_recommended = sum_not_recommended
        self.game_id = game_id

    def to_dict(self) -> dict[str, TimeInterval | int]:
        return {
            "time_interval": self.time_interval,
            "sum_recommended": self.sum_recommended,
            "sum_not_recommended": self.sum_not_recommended
        }
