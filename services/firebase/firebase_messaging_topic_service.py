from firebase_admin import messaging

from globals.utils import WxLogger
from notification.dto.common.message_dto import FirebaseTopicMessageDto

_logger = WxLogger(__name__).getLogger()


class FirebaseMessagingTopicService:
    @classmethod
    def subscribe_to_topic(
        cls,
        topic_name: str,
        tokens=None,
    ):
        if not tokens:
            return False
        return messaging.subscribe_to_topic(
            tokens=tokens,
            topic=topic_name,
        )

    @classmethod
    def unsubscribe_from_topic(
        cls,
        topic_name: str,
        tokens=None,
    ):
        if not tokens:
            return False

        return messaging.unsubscribe_from_topic(
            tokens=tokens,
            topic=topic_name,
        )

    @classmethod
    def send_message_to_topic(
        cls,
        topic_name: str,
        data: FirebaseTopicMessageDto,
    ):
        """
        data : {
            "title": "asdasd",
            "body": "asdasd",
            "analytics_label": "analytics_label",
            "deep_link": "deep_link",
            "banner_image": "banner_image",
            "badge_image": "badge_image",
        }
        """
        message = messaging.Message(
            topic=topic_name,
            data=data.simple_dict(),
        )
        response = messaging.send(message)
        return response
