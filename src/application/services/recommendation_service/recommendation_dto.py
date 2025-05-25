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

    def to_dict(self) -> dict[str, int]:
        return {
            "time_interval": self.time_interval.value,
            "sum_recommended": int(self.sum_recommended),
            "sum_not_recommended": int(self.sum_not_recommended)
        }


@dataclass
class FinalResultDto:
    game_id: int
    correlation_id: str
    recommendations: list[RecommendationDto]

    def __init__(
            self,
            game_id: int,
            correlation_id: str,
            recommendations: dict[str, tuple[float, float]] | list[RecommendationDto]
    ):
        self.game_id = game_id
        self.correlation_id = correlation_id
        if isinstance(recommendations, dict):
            recommendation_dtos: list[RecommendationDto] = []
            for key, values in recommendations.items():
                sum_recommended, sum_not_recommended = values
                dto = RecommendationDto(
                    time_interval=key,
                    sum_recommended=sum_recommended,
                    sum_not_recommended=sum_not_recommended
                )

                recommendation_dtos.append(dto)

            self.recommendations = recommendation_dtos
        else:
            self.recommendations = recommendations

    def to_dict(self) -> dict[str, int | str | list[dict[str, int]]]:
        return {
            "game_id": self.game_id,
            "correlation_id": self.correlation_id,
            "recommendations": [recommendation.to_dict() for recommendation in self.recommendations]
        }
