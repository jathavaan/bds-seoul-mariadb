from dataclasses import dataclass
from datetime import datetime

from src.application.services.recommendation_service import FinalResultDto


@dataclass
class GameDto:
    pass


@dataclass
class LastScrapedDateRequestDto:
    game_id: int
    correlation_id: str


@dataclass
class LastScrapedDateResponseDto:
    steam_game_id: int
    last_scraped_date: datetime | None
    result: FinalResultDto | None
    correlation_id: str

    def to_dict(self) -> dict:
        return {
            "steam_game_id": self.steam_game_id,
            "last_scraped_date": self.last_scraped_date.strftime(
                "%Y-%m-%d-%H-%M-%S"
            ) if self.last_scraped_date else None,
            "result": self.result.to_dict() if self.result else None,
            "correlation_id": self.correlation_id
        }
