import logging
from typing import Sequence

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.domain.entities import Recommendation
from .recommendation_dto import RecommendationDto


class RecommendationRepositoryService:
    __db_session: Session
    __logger: logging.Logger

    def __init__(self, db_session: Session, logger: logging.Logger):
        self.__db_session = db_session
        self.__logger = logger

    def get_recommendations_by_game_id(self, game_id: int) -> Sequence[Recommendation]:
        return self.__db_session.scalars(
            select(Recommendation).where(
                Recommendation.game_id == game_id
            )
            .order_by(Recommendation.time_interval.asc())
        ).all()

    def insert_recommendations(self, recommendations: list[Recommendation]) -> None:
        self.__db_session.add_all(recommendations)
        self.__db_session.commit()
        self.__logger.info(f"Inserted {len(recommendations)} recommendations")

    def upsert_result(self, game_id: int, recommendation_dtos: list[RecommendationDto]) -> bool:
        recommendations = list(self.get_recommendations_by_game_id(game_id))
        if len(recommendations) == 0:
            for dto in recommendation_dtos:
                recommendation = Recommendation(
                    game_id=game_id,
                    time_interval=dto.time_interval,
                    sum_recommended=int(dto.sum_recommended),
                    sum_not_recommended=int(dto.sum_not_recommended)
                )

                recommendations.append(recommendation)

            self.insert_recommendations(recommendations)
        else:
            if len(recommendations) != len(recommendation_dtos):
                self.__logger.error(
                    f"Failed to update recommendations for game [internal game ID: {game_id}]. Found {len(recommendations)} records in DB, but received {len(recommendation_dtos)} records to update"
                )
                return False

            recommendations.sort(key=lambda x: x.time_interval)
            recommendation_dtos.sort(key=lambda x: x.time_interval)

            for (entity, dto) in zip(recommendations, recommendation_dtos):
                entity.sum_recommended += int(dto.sum_recommended)
                entity.sum_not_recommended += int(dto.sum_not_recommended)

            self.__db_session.commit()

        return True
