from datetime import datetime

from pydantic import BaseModel

music_file_example = {
    "_id": "12952",
    "name": "12842lalsdfa.wav",
    "sample_width": 2,
    "rate": 44100,
    "channels": 2,
    "size": 5023999,
}

music_example = {
    "_id": 112452,
    "name": "다시만난세계",
    "singer": "소녀시대",
    "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
    "play_total": 128,
    "file": music_file_example,
}


class MusicFile(BaseModel):
    _id: int
    name: str
    sample_width: int
    rate: int
    channels: int
    size: int

    class Config:
        schema_extra = {
            "example": music_file_example,
        }


class Music(BaseModel):
    _id: int
    name: str
    singer: str
    release_data: datetime
    play_total: int
    file: MusicFile

    class Config:
        schmea_extra = {
            "example": music_example,
        }
