from emoji import emojize
from utils.exceptions import SystemExitException
from settings.env import Environments, EnvironmentService
from .setting import Settings
from utils.wxlogger import WxLogger
import logging

log = WxLogger(__name__).getLogger()


class EmojiLogger:
    logger: logging.Logger = None

    def __init__(self):
        if self.__class__.logger is None:
            self.__class__.logger = WxLogger(self.__class__.__name__).getLogger()

    def success(self):
        self.__class__.logger.info(emojize(":thumbs_up:") * 40)

    def debug(self):
        self.__class__.logger.info(emojize(":red_heart:") * 40)

    def error(self):
        self.__class__.logger.info(emojize(":skull:") * 40)


class SettingsFactory:
    wxsettings: Settings = None
    elogger = EmojiLogger()

    def __init__(self, environment: Environments = Environments.LOCALHOST):
        if environment.value not in Environments.list():
            self.__class__.elogger.error()
            raise SystemExitException(message=f"ENV: <{environment.value}> Doesn't Exists")
        self.__class__.elogger.success()
        log.info(f"ENVIRONMENT: {environment}")
        self.__class__.elogger.success()
        if environment == Environments.DEVELOPMENT:
            from settings.setting_development import Settings
            self.wxsettings = Settings()
        elif environment == Environments.LOCALHOST:
            from settings.setting_localhost import Settings
            self.wxsettings = Settings()
        elif environment == Environments.PRODUCTION:
            from settings.setting_production import Settings
            self.wxsettings = Settings()
        EnvironmentService(environment=environment)

    def get_settings(self):
        return self.wxsettings
