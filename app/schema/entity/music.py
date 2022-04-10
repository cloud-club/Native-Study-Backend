import typing as t
from datetime import datetime

from pydantic import BaseModel

from app.schema.entity.pyobject import PydanticObjectId

music_file_example = {
    "name": "12842lalsdfa.wav",
    "length": 58.09,
    "rate": 44100,
    "channels": 2,
    "path": "/music/12842lalsdfa.wav",
    "size": 10406738,
}

music_in_db_example = {
    "name": "다시만난세계",
    "singer": "소녀시대",
    "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
    "play_total": 128,
    "file_id": "6251a09f19578b34a0ffc6f",
}

music_example = {
    "name": "다시만난세계",
    "singer": "소녀시대",
    "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
    "play_total": 128,
    "file": music_file_example,
}


class MusicFile(BaseModel):
    name: str
    length: float
    rate: int
    channels: int
    path: str
    size: int

    class Config:
        schema_extra = {
            "example": music_file_example,
        }


class MusicInDB(BaseModel):
    name: str
    singer: str
    release_date: t.Optional[str]
    play_total: int = 0
    file_id: PydanticObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PydanticObjectId: lambda v: str(v)}
        schema_extra = {
            "example": music_in_db_example,
        }


class Music(BaseModel):
    name: str
    singer: str
    release_date: t.Optional[str]
    play_total: int
    file: MusicFile

    class Config:
        schmea_extra = {
            "example": music_example,
        }
