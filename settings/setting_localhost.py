import os

from .setting import Settings as BaseSettings
from .setting import BASE_DIR, SETTINGS_DIR
from .env.env_service import Environments


class Settings(BaseSettings):
    enviroment = Environments.LOCALHOST
    app_name: str = "Awesome API"
    admin_email: str = "tarun@wx.com"
    BASE_DIRECTORY = BASE_DIR
    # Service Account Path
    SERVICE_ACCOUNT = os.path.join(SETTINGS_DIR, "facex", "credentials", "service_account.json")
    # GCS  BUCKET
    GCS_BUCKET = "wx_pokemon"
    # GCS  CACHING
    GCS_CACHING = 0  # 60 * 60 * 24 * 365
    ALLOWED_HOSTS = ["localhost", "*.example.com", "thanos.in.ngrok.io"]
    # INFRA URLs & PORTS
    BROKERS = ["amqp://guest:guest@localhost:15672//"]
    CELERY_NAME = "facex"
    CELERY_RESULTS_TTL_SECS = 60000
    MONGODB_URL = "mongodb://mongo:VvboIwH9rzvUAT9RNTRjR4oURBBKuj7dHaLNfCxMtLDkoxaFEJLWn8UcUL3jOsPP9suHDaZmKSnp2pHrmYHSuzdGiRBT3VL26ABubOTHlSIa3oVkwHRJXjG31QmugFIJ@localhost:37017/workex?authSource=admin"
    MONGODB_NAME = "workex"
    ELASTICSEARCH_HOSTS = "http://localhost:4210/"