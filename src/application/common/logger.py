import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    _instances = {}

    @staticmethod
    def get_logger(
            name: str,
            log_file: str = os.path.join("logs", "app.log"),
            level: int = logging.INFO
    ) -> logging.Logger:
        """
        Returns a logger instance. Ensures that loggers are reused across the project.

        :param name: Name of the logger.
        :param log_file: Path to the log file.
        :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :return: Configured logger instance.
        """
        if name in Logger._instances:
            return Logger._instances[name]

        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)

        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.propagate = False

        Logger._instances[name] = logger
        return logger
