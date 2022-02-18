from firebase_admin import initialize_app
from firebase_admin import messaging

from globals.exceptions import ValidationException
from globals.utils import WxLogger


class FirebaseMessaging:
    _client: messaging = None
    logger = None

    @property
    def client(self):
        FirebaseMessaging.logger.debug("Giving firebase messaging client")
        return FirebaseMessaging._client

    @client.setter
    def client(self, value):
        if type(value) == messaging and not FirebaseMessaging._client:
            FirebaseMessaging._client = value
        else:
            raise ValidationException(message="Firebase Configuration Issue")

    def __init__(self):
        if not FirebaseMessaging.logger:
            FirebaseMessaging.logger = WxLogger(__name__).getLogger()

        if not FirebaseMessaging._client:
            initialize_app()
            FirebaseMessaging.logger.info("Initialization of Firebase Firestore")
            FirebaseMessaging._client = messaging
