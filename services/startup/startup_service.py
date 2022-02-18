from globals.exceptions import RunTimeException
from globals.services.project.elastic import ElasticClient
from globals.services.project.env import EnvironmentService
from globals.services.project.firebase import Firestore
from globals.services.project.google_application_credentials import (
    GoogleApplicationCredentials,
)
from globals.services.project.google_storage import GoogleStorage
from globals.services.project.redis.client import RedisClient
from globals.utils import WxLogger


class StartUpService:
    started: bool = None
    logger = None

    def __init__(self):
        if StartUpService.started is None:
            StartUpService.logger = WxLogger(__name__).getLogger()
            StartUpService.started = True
            StartUpService.logger.info("========================================")
            StartUpService.logger.info("\u2620" * 40)
            ElasticClient()
            EnvironmentService()
            GoogleApplicationCredentials()
            Firestore()
            GoogleStorage()
            RedisClient()
            StartUpService.logger.info("\u2620" * 40)
            StartUpService.logger.info("========================================")
        else:
            raise RunTimeException()
