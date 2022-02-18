from firebase_admin.firestore import firestore

from globals.exceptions import ValidationException
from globals.utils import WxLogger


class Firestore:
    _client: firestore.Client = None
    logger = None

    @property
    def client(self):
        Firestore.logger.debug("Giving firestore client")
        return Firestore._client

    @client.setter
    def client(self, value: firestore.Client):
        if type(value) == firestore.Client and not Firestore._client:
            Firestore._client = value
        else:
            raise ValidationException(message="Firebase Configuration Issue")

    def __init__(self):
        if not Firestore.logger:
            Firestore.logger = WxLogger(__name__).getLogger()

        if not Firestore._client:
            Firestore.logger.info("Initialization of Firebase Firestore")
            Firestore._client = firestore.Client()
