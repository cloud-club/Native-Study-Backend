from pydantic import BaseSettings


class settings(BaseSettings):
    # Base Env
    APP_ENV: str

    # minIO
    MINIO_HOST_NAME: str
    MINIO_API_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str

    # music service
    MUSIC_SERVICE_INTERNAL_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = settings()
