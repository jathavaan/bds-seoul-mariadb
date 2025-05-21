from src.application import Container
from src.entrypoints.consumers import MapreduceResultConsumer, LastScrapedDateConsumer

container = Container()

logger = container.logger()
game_repository_service = container.game_repository_service()
recommendation_repository_service = container.recommendation_repository_service()


def main() -> None:
    last_scraped_date_consumer = LastScrapedDateConsumer(
        logger=logger,
        game_repository_service=game_repository_service
    )

    mapreduce_result_consumer = MapreduceResultConsumer(
        logger=logger,
        game_repository_service=game_repository_service,
        recommendation_repository_service=recommendation_repository_service
    )

    try:
        while True:
            is_response_ready, last_scraped_date_response = last_scraped_date_consumer.consume()
            if is_response_ready:
                pass  # TODO: Call last_scraped_date_producer.produce() here

            mapreduce_result_consumer.consume()
    except KeyboardInterrupt:
        pass
    finally:
        mapreduce_result_consumer.close()


if __name__ == "__main__":
    main()
