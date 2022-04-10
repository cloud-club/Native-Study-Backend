from pydantic import BaseSettings


class settings(BaseSettings):
    # Base Env
    APP_ENV: str

    # minIO
    MINIO_HOST_NAME: str
    MINIO_API_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_REGION: str = "ap-northeast-2"
    MINIO_USE_TLS: bool = False

    # music service
    MUSIC_SERVICE_INTERNAL_PORT: int

    # mongoDB
    MONGO_HOST_NAME: str
    MONGO_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    DATABASE_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = settings()
