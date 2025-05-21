from dataclasses import dataclass

from src.domain.enums import TimeInterval


@dataclass
class RecommendationDto:
    time_interval: TimeInterval
    sum_recommended: float
    sum_not_recommended: float

    def __post_init__(self) -> None:
        if isinstance(self.time_interval, str):
            self.time_interval = TimeInterval.from_value(self.time_interval)
