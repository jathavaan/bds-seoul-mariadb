from src.entrypoints import MariaDbConsumer


def main() -> None:
    pass


if __name__ == "__main__":
    consumer = MariaDbConsumer()
    try:
        consumer.consume()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
