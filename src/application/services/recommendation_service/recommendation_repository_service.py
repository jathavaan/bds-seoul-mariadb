import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities import Recommendation
from src.domain.enums import TimeInterval
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

            for interval in TimeInterval:
                if interval not in [dto.time_interval for dto in recommendation_dtos]:
                    recommendation = Recommendation(
                        game_id=game_id,
                        time_interval=interval,
                        sum_recommended=0,
                        sum_not_recommended=0
                    )

                    recommendations.append(recommendation)

            self.insert_recommendations(recommendations)
        else:
            number_of_recommendations = len(recommendations)
            number_of_recommendation_dtos = len(recommendation_dtos)
            if number_of_recommendations != number_of_recommendation_dtos:
                self.__logger.warning(
                    f"Game [internal game ID: {game_id}] received {number_of_recommendation_dtos} recommendations, but {number_of_recommendations} already exist in the database. This is not an error, but is rare and should be investigated."
                )

                if number_of_recommendations > number_of_recommendation_dtos:
                    for time_interval in TimeInterval:
                        if time_interval not in [
                            recommendation_dto.time_interval for recommendation_dto in recommendation_dtos
                        ]:
                            recommendation_dtos.append(RecommendationDto(
                                time_interval=time_interval,
                                sum_recommended=0,
                                sum_not_recommended=0
                            ))
                elif number_of_recommendations < number_of_recommendation_dtos:
                    recommendations_to_add: list[Recommendation] = []
                    for time_interval in TimeInterval:
                        if time_interval not in [
                            recommendation.time_interval for recommendation in recommendations
                        ]:
                            empty_recommendation = Recommendation(
                                game_id=game_id,
                                time_interval=time_interval,
                                sum_recommended=0,
                                sum_not_recommended=0
                            )

                            recommendations.append(empty_recommendation)
                            recommendations_to_add.append(empty_recommendation)

                    if recommendations_to_add:
                        self.__db_session.add_all(recommendations_to_add)

            recommendations.sort(key=lambda x: x.time_interval.value)
            recommendation_dtos.sort(key=lambda x: x.time_interval.value)

            for (entity, dto) in zip(recommendations, recommendation_dtos):
                entity.sum_recommended += int(dto.sum_recommended)
                entity.sum_not_recommended += int(dto.sum_not_recommended)

            self.__db_session.commit()

        return True
