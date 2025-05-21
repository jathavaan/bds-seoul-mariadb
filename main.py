from src.application import Container
from src.entrypoints.consumers import MapreduceResultConsumer

container = Container()

logger = container.logger()
game_repository_service = container.game_repository_service()
recommendation_repository_service = container.recommendation_repository_service()


def main() -> None:
    mapreduce_result_consumer = MapreduceResultConsumer(
        logger=logger,
        game_repository_service=game_repository_service,
        playtime_recommendation_repository_service=recommendation_repository_service
    )

    try:
        while True:
            mapreduce_result_consumer.consume()
    except KeyboardInterrupt:
        pass
    finally:
        mapreduce_result_consumer.close()


if __name__ == "__main__":
    main()
