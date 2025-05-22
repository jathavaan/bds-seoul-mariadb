from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameDto:
    pass


@dataclass
class LastScrapedDateRequestDto:
    game_id: int


@dataclass
class LastScrapedDateResponseDto:
    steam_game_id: int
    last_scraped_date: datetime | None

    def to_dict(self) -> dict:
        return {
            "steam_game_id": self.steam_game_id,
            "last_scraped_date": self.last_scraped_date.strftime(
                "%Y-%m-%d-%H-%M-%S"
            ) if self.last_scraped_date else None
        }
