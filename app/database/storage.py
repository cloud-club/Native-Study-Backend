import typing as t
from io import BytesIO

from minio import Minio, S3Error, api
from urllib3.response import HTTPResponse

from app.common.config import settings


class Storage:
    _client: t.Optional[api.Minio] = None

    def __init__(
        self,
        host: str,
        port: int,
        access_key: str,
        secret_key: str,
        region: str,
        secure: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.secure = secure

    def connect(self):
        if self._client is None:
            self._client = Minio(
                endpoint=f"{self.host}:{self.port}",
                access_key=self.access_key,
                secret_key=self.secret_key,
                region=self.region,
                secure=self.secure,
            )
        self.validator()
        return self._client

    def validator(self) -> bool:
        try:
            if "music" not in self._client.list_buckets():
                self._client.make_bucket("music")
        except S3Error:
            raise ValueError("connection error: 서버 정보가 올바르지 않습니다.")

    def save(
        self, bucket_name: str, object_name: str, binary: BytesIO, length: int
    ) -> bool:
        try:
            self._client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=binary,
                length=length,
            )
        except:
            # @TODO: subdivide exception case and logging
            return False
        return True

    def load(self, bucket_name: str, object_name: str) -> t.Optional[HTTPResponse]:
        try:
            response = self._client.get_object(
                bucket_name=bucket_name, object_name=object_name
            )
        except:
            return None
        finally:
            response.close()
            response.release_conn()
        return response


storage = Storage(
    host=settings.MINIO_HOST_NAME,
    port=settings.MINIO_API_PORT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    region=settings.MINIO_REGION,
    secure=settings.MINIO_USE_TLS,
)
