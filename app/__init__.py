from minio import Minio
from rich import inspect
from rich.console import Console

from app.common.config import settings

console = Console()
print = console.log
dprint = inspect


class FileStorage:
    _client = None

    def __init__(
        self,
        url: str,
        access_key: str,
        secret_key: str,
        region: str,
        secure: bool = True,
    ):
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.secure = secure

    def connect(self):
        if self._client is None:
            self._client = Minio(
                self.urk, self.access_key, self.secret_key, self.region, self.secure
            )
        if "music" not in self._client.list_buckets():
            self._client.make_bucket("music")

        return self._client


file_server = FileStorage(
    f"{settings.MINIO_HOST_NAME}:{settings.MINIO_API_PORT}",
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    region=settings.MINIO_REGION,
    secure=False,
)
