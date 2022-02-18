import datetime

import magic
from google.cloud import storage
from PIL.Image import Image

from globals.exceptions import ValidationException
from globals.utils import WxLogger
from wx_hrms.settings import GOOGLE_STORAGE


class GoogleStorage:
    _client: storage.Client = None
    logger = None
    GOOGLE_STORAGE_BASE_URL = "https://storage.googleapis.com"

    @property
    def client(self):
        GoogleStorage.logger.debug("Giving google client")
        return GoogleStorage._client

    @client.setter
    def client(self, value: storage.Client):
        if type(value) == storage.Client and not GoogleStorage._client:
            GoogleStorage._client = value
        else:
            raise ValidationException(message="Google Configuration Issue")

    def __init__(self):
        if not GoogleStorage.logger:
            GoogleStorage.logger = WxLogger(__name__).getLogger()

        if not GoogleStorage._client:
            GoogleStorage.logger.info("Initialization of Google Storage")
            GoogleStorage._client = storage.Client()

    def upload_from_file(
        self,
        file_object,
        file_name: str,
        gcs_bucket: str = None,
    ) -> str:
        if gcs_bucket is None:
            GOOGLE_STORAGE.get("bucket")
        bucket = self.client.bucket(gcs_bucket)
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(file_name)
        blob = bucket.blob(f"{file_name}")
        blob.upload_from_file(file_object)
        blob.content_type = content_type
        blob.cache_control = f"public, max-age={GOOGLE_STORAGE.get('cache')}"
        blob.patch()
        blob.make_public()
        return blob.public_url

    def upload_image(self, image: Image, file_name: str, gcs_bucket: str = None) -> str:
        if gcs_bucket is None:
            gcs_bucket = GOOGLE_STORAGE.get("bucket")
        bucket = self.client.bucket(gcs_bucket)
        blob = bucket.blob(f"{file_name}.{image.format.lower()}")
        from io import BytesIO

        arr = BytesIO()
        image.save(arr, format=image.format)
        blob.upload_from_string(arr.getvalue())
        img_format = image.format
        blob.content_type = f"image/{img_format.lower()}"
        blob.cache_control = f"public, max-age={GOOGLE_STORAGE.get('cache')}"
        blob.patch()
        blob.make_public()
        return blob.public_url

    def upload_from_string(
        self,
        content,
        file_name: str,
        content_type: str = None,
        folder: str = None,
        gcs_bucket: str = None,
        public: bool = True,
    ) -> str:
        if gcs_bucket is None:
            gcs_bucket = GOOGLE_STORAGE.get("bucket")
        bucket = self.client.bucket(gcs_bucket)
        if not content_type:
            mime = magic.Magic(mime=True)
            content_type = mime.from_buffer(content)

        if folder:
            file_name = f"{folder}/{file_name}"
        else:
            file_name = file_name
        blob = bucket.blob(f"{file_name}")
        blob.upload_from_string(content)
        blob.content_type = content_type
        blob.cache_control = f"public, max-age={GOOGLE_STORAGE.get('cache')}"
        blob.patch()
        if public:
            blob.make_public()
            return blob.public_url
        return f"https://storage.googleapis.com/{gcs_bucket}/{file_name}"

    def download_file(self, cloud_file_path: str, bucket: str = None):
        if not bucket:
            bucket = GOOGLE_STORAGE.get("bucket")
        gcs_bucket = self.client.bucket(bucket)
        blob = gcs_bucket.blob(cloud_file_path)
        bytes_data = blob.download_as_bytes()
        return bytes_data

    def generate_download_signed_url_v4(self, bucket_name, blob_name):
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(seconds=30),
            method="GET",
        )
        return url

    def upload_public_from_file_path(
        self,
        absolute_path: str,
        subdir: str,
        file_name: str,
    ):
        bucket = self.client.get_bucket(GOOGLE_STORAGE.get("bucket"))
        blob = bucket.blob(f"{subdir}/{file_name}")
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(f"{absolute_path}")
        blob.upload_from_filename(
            filename=f"{absolute_path}",
            content_type=content_type,
        )
        blob.cache_control = f"public, max-age=100000"
        blob.patch()
        blob.make_public()
        uploaded_url = (
            f"{self.GOOGLE_STORAGE_BASE_URL}/{bucket.name}/{subdir}/{file_name}"
        )
        return uploaded_url
