from pymongo import MongoClient, mongo_client

from app.common.config import settings
from app.common.type import t


class NoSQL:
    host: str
    port: int
    username: str
    password: str

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self) -> None:
        raise NotImplementedError


class Mongo(NoSQL):
    _client: t.Optional[mongo_client.MongoClient] = None

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        super().__init__(host=host, port=port, username=username, password=password)

    def connect(self) -> mongo_client.MongoClient:
        if self._client is None:
            self._client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
        return self._client


db = Mongo(
    host=settings.MONGO_HOST_NAME,
    port=settings.MONGO_PORT,
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD,
)


def get_db():
    session = db.connect()
    return session[settings.DATABASE_NAME]
