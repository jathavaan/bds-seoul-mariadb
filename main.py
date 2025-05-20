from src.entrypoints.consumers import MariaDbConsumer, MapreduceResultConsumer


def main() -> None:
    pass


if __name__ == "__main__":
    try:
        maria_db_consumer = MariaDbConsumer()
        # mapreduce_result_consumer = MapreduceResultConsumer()

        while True:
            continue
            maria_db_consumer.consume()
    except KeyboardInterrupt:
        pass
    finally:
        maria_db_consumer.close()
