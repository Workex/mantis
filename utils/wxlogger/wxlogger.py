import logging

import coloredlogs


class Levels:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    @staticmethod
    def get_level(name):
        if name == Levels.DEBUG:
            return 10
        if name == Levels.INFO:
            return 20
        if name == Levels.WARNING:
            return 30
        if name == Levels.ERROR:
            return 40
        if name == Levels.CRITICAL:
            return 50
        raise Exception("UndefinedLevel")


class WxLogger:
    """Logger Class."""

    def format_log_name(self, name: str):
        format = name.split(".")
        _format = ".".join(format[:2])
        length = 50 - len(_format) - len(format[-1])
        _format = f"{_format}{'.' * length}{format[-1]}"
        return _format

    def __init__(self, name=__name__, config=None):
        """Constructor which initializes the logger for the module.

        :rtype: None
        :param (name:str) logger name for identification
        :param (config:object)
            config['level'] = logging level [DEBUG, ERROR, WARNING, INFO, CRITICAL] Default DEBUG
        """
        try:
            if config is None:
                config = {"level": Levels.DEBUG}
            if len(name) > 50:
                name = self.format_log_name(name)
            self.logger = logging.getLogger(name)
            self.level = Levels.get_level(config["level"])

            self.logger.setLevel(self.level)

            formatter = "%(levelname)-1s: %(asctime)s [%(name)s:%(lineno)1d] %(message)s"
            coloredlogs.install(
                level=config["level"],
                logger=self.logger,
                fmt=formatter,
            )
            self.logger.log(self.level, f"{name} logger initiated")
        except Exception as ex:
            self.logger.error(str(ex))

    def getLogger(self) -> logging.Logger:
        """Return the logger instance."""
        return self.logger
