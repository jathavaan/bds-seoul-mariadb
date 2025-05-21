from dataclasses import dataclass


@dataclass
class PlaytimeRecommendationDto:
    time_interval: str
    sum_recommended: float
    sum_not_recommended: float
