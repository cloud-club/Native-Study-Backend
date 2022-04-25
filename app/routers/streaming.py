import wave

import pyaudio
from bson.objectid import ObjectId
from fastapi import APIRouter, Query, status
from fastapi.responses import StreamingResponse

from app import inspect, mc
from app.common.type import t
from app.database.connect import get_db
from app.schema.response import music as music_resp

router = APIRouter()

CHUNK = 1024


async def load_wav_stream(binary: bytes) -> t.Generator:
    """ file storage로부터 음악 bytes를 읽어옵니다.
    """
    wave_io = wave.open(binary)
    data = wave_io.readframes(CHUNK)
    while data:
        try:
            yield data
            data = wave_io.readframes(CHUNK)
        except:
            break


@router.get(
    "/",
    responses={
        200: {"model": music_resp.StreamMusicResponse, "description": "요청한 음악을 스트리밍"},
    },
    status_code=status.HTTP_200_OK,
)
async def stream_music(
    music_name: str = Query(..., description="음악 이름"),
    singer_name: str = Query(None, description="가수 이름"),
) -> StreamingResponse:
    """요청한 음악을 스트리밍합니다."""
    music_filter = dict(name=music_name)
    if singer_name:
        music_filter.update(dict(singer=singer_name))

    # init db
    db = get_db()

    musicDB = db.music
    music_data = musicDB.find_one(music_filter)

    file_id = ObjectId(music_data["file_id"])
    fileDB = db.file
    file_data = fileDB.find_one(dict(_id=file_id))

    response = mc.get_object("music", file_data["name"])

    return StreamingResponse(content=load_wav_stream(response))
