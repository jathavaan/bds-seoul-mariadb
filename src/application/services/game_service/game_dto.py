from dataclasses import dataclass
from datetime import datetime


@dataclass
class GameDto:
    pass


@dataclass
class LastScrapedDateDto:
    game_id: int
    steam_game_id: int
    last_scraped_date: datetime
