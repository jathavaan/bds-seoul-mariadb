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
