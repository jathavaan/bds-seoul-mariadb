import logging
from typing import Sequence

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.application.services.playtime_recommendation_service import PlaytimeRecommendationDto
from src.domain.entities import PlaytimeRecommendation


class PlaytimeRecommendationRepositoryService:
    __db_session: Session
    __logger: logging.Logger

    def __init__(self, db_session: Session, logger: logging.Logger):
        self.__db_session = db_session
        self.__logger = logger

    def get_playtime_recommendations_by_game_id(self, game_id: int) -> Sequence[PlaytimeRecommendation]:
        return self.__db_session.scalars(
            select(PlaytimeRecommendation).where(
                PlaytimeRecommendation.game_id == game_id
            )
            .order_by(PlaytimeRecommendation.time_interval.asc())
        ).all()

    def insert_recommendations(self, recommendations: list[PlaytimeRecommendation]) -> None:
        self.__db_session.add_all(recommendations)
        self.__db_session.commit()
        self.__logger.info(f"Inserted {len(recommendations)} recommendations")

    def upsert_result(self, game_id: int, playtime_recommendation_dtos: list[PlaytimeRecommendationDto]) -> bool:
        playtime_recommendations = list(self.get_playtime_recommendations_by_game_id(game_id))
        if len(playtime_recommendations) == 0:
            for dto in playtime_recommendation_dtos:
                recommendation = PlaytimeRecommendation(
                    game_id=game_id,
                    time_interval=dto.time_interval,
                    sum_recommended=int(dto.sum_recommended),
                    sum_not_recommended=int(dto.sum_not_recommended)
                )

                playtime_recommendations.append(recommendation)

            self.insert_recommendations(playtime_recommendations)
        else:
            if len(playtime_recommendations) != len(playtime_recommendation_dtos):
                self.__logger.error(
                    f"Failed to update recommendations for game [internal game ID: {game_id}]. Found {len(playtime_recommendations)} records in DB, but received {len(playtime_recommendation_dtos)} records to update"
                )
                return False

            playtime_recommendations.sort(key=lambda x: x.time_interval)
            playtime_recommendation_dtos.sort(key=lambda x: x.time_interval)

            for (entity, dto) in zip(playtime_recommendations, playtime_recommendation_dtos):
                entity.sum_recommended += int(dto.sum_recommended)
                entity.sum_not_recommended += int(dto.sum_not_recommended)

            self.__db_session.commit()

        return True
