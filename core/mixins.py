import logging


class LoggingMixin:

    __slots__ = ()

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
        return logger

    def log(self, message: str) -> None:
        self._get_logger().info(
            f"[{self.__class__.__name__}] INFO: {message}"
        )

    def log_warning(self, message: str) -> None:
        self._get_logger().warning(
            f"[{self.__class__.__name__}] WARNING: {message}"
        )

    def log_error(self, message: str) -> None:
        self._get_logger().error(
            f"[{self.__class__.__name__}] ERROR: {message}"
        )
