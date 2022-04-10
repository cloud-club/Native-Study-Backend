import typing as t
from io import BytesIO

from minio import Minio, S3Error, api
from urllib3.response import HTTPResponse

from app.common.config import settings


class Storage:
    client: api.Minio

    def __init__(
        self,
        host: str,
        port: int,
        access_key: str,
        secret_key: str,
        region: str,
        secure: bool,
    ) -> None:
        self.client = Minio(
            endpoint=f"{host}:{port}",
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            secure=secure,
        )
        self.validator()

    def validator(self) -> bool:
        try:
            self.client.list_buckets()
        except S3Error:
            raise ValueError("connection error: 서버 정보가 올바르지 않습니다.")

    def save(
        self, bucket_name: str, object_name: str, binary: BytesIO, length: int
    ) -> bool:
        try:
            self.client.put_object(
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
            response = self.client.get_object(
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
