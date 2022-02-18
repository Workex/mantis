import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings:
    enviroment = "base"
    app_name: str = "Awesome API"
    admin_email: str = "tarun@wx.com"
    BASE_DIRECTORY = SETTINGS_DIR
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
    MONGODB_URL = "mongodb://mongoadmin:mongoadmin@localhost:27018/wx_managed?authSource=admin&retryWrites=true&w=majority"
    MONGODB_NAME = "wx_managed"
    ELASTICSEARCH_HOSTS = "http://localhost:9200"
