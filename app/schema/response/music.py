import typing as t
from uuid import uuid4

from pydantic import BaseModel

from app.schema.entity.music import Music, music_example
from app.schema.response.common import BaseResponse, response_metadata


class UploadMusicResponse(BaseResponse):
    class Config:
        schema_extra = {
            "example": {
                "request_metadata": {
                    "request_id": str(uuid4()),
                    "request_data": {
                        "music_name": "다시만난세계",
                        "singer_name": "소녀시대",
                        "release_date": "2022-07-25",
                        "music_file": "/Music/[효과음]BOING #2.mp3",
                    },
                },
                "response_metadata": response_metadata,
            }
        }


class MusicResponse(BaseResponse):
    music: Music

    class Config:
        schema_extra = {
            "example": {
                "request_metadata": {
                    "request_id": str(uuid4()),
                    "request_data": {
                        "offset": "1-2,5",
                    },
                },
                "response_metadata": response_metadata,
                "music": music_example,
            }
        }


class MusicChartResponse(BaseResponse):
    musics: t.List[Music]

    class Config:
        schema_extra = {
            "example": {
                "request_metadata": {
                    "request_id": str(uuid4()),
                    "request_data": {
                        "offset": "1-2,5",
                    },
                },
                "response_metadata": response_metadata,
                "musics": [
                    music_example,
                ],
            }
        }


class StreamMusicResponse(BaseModel):
    _content: bytes

    class Config:
        schema_extra = {
            "example": {
                "_content": "?\x02\xce\xeaB\x03\x97\xe9\x1c\x04\xb0\xec\x13",
            },
        }
