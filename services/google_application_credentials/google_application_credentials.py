import os

from firebase_admin import initialize_app

from wx_hrms.settings import BASE_DIR
from wx_hrms.settings import GOOGLE_CREDENTIAL_PATH


class GoogleApplicationCredentials:
    def __init__(self):
        if not os.path.exists(BASE_DIR + f"/{GOOGLE_CREDENTIAL_PATH}"):
            raise Exception(
                "Firebase service account not found, must be present in PATH : wx_hrms/service_account.json",
            )
        os.environ.setdefault(
            "GOOGLE_APPLICATION_CREDENTIALS",
            BASE_DIR + f"/{GOOGLE_CREDENTIAL_PATH}",
        )
        initialize_app()
