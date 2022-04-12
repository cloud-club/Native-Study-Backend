from minio import Minio
from rich import inspect
from rich.console import Console

from app.common.config import settings

console = Console()
print = console.log
dprint = inspect

mc = Minio(
    f"{settings.MINIO_HOST_NAME}:{settings.MINIO_API_PORT}",
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    region=settings.MINIO_REGION,
    secure=False,
)

if "music" not in mc.list_buckets():
    mc.make_bucket("music")
