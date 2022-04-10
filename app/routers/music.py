from datetime import datetime
from uuid import uuid4

from bson.objectid import ObjectId
from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.database.connect import db
from app.schema.entity.file import AudioFile
from app.schema.entity.music import Music, MusicFile, MusicInDB
from app.schema.response import music as music_resp
from app.schema.response.common import RequestMetadata, ResponseMetadata
from app.utils.time import elapsed, time2str

router = APIRouter()


@router.post(
    "/musics",
    responses={
        201: {
            "model": music_resp.UploadMusicResponse,
            "description": "정상적으로 요청을 처리한 케이스",
        },
        415: {"description": "지원하지 않는 포맷입니다."},
    },
)
async def upload_music(
    music_name: str = Form(...),
    singer_name: str = Form(...),
    release_date: str = Form(None),
    music_file: UploadFile = File(...),
) -> JSONResponse:
    """음악 파일과 음악 메타정보를 저장 합니다.

    Args:
        music_name (str): 음악 이름.
        singer_name (str): 가수 이름.
        release_date (str, Optional): 발매 일자.
        music_file (UploadFile): 음악 파일.

    Returns:
        JSONResponse:
            request_metadata (dict): 요청 정보
            response_metadata (dict): 응답 처리 정보
    """
    request_time = datetime.now()
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data={
            "music_name": music_name,
            "singer_name": singer_name,
            "release_date": release_date,
            "music_file": music_file.filename,
        },
    )

    # file validation
    binary = await music_file.read()
    audio_file = AudioFile(binary, content_type=music_file.content_type)

    # save file in minIO
    path = await audio_file.save(music_file.filename)

    # save data in DB
    metadata = MusicFile(
        name=music_file.filename,
        path=path,
        **audio_file.metadata,
    )
    fileDB = db.file
    file_id = fileDB.insert_one(metadata.dict()).inserted_id
    music = MusicInDB(
        name=music_name,
        singer=singer_name,
        release_date=release_date,
        play_total=0,
        file_id=file_id,
    )
    musicDB = db.music
    musicDB.insert_one(music.dict())

    response_time = datetime.now()
    response_metadata = ResponseMetadata(
        request_time=time2str(request_time),
        response_time=time2str(response_time),
        elapsed_time=elapsed(request_time, response_time),
    )
    response = music_resp.UploadMusicResponse(
        request_metadata=request_metadata,
        response_metadata=response_metadata,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(response),
    )


@router.get(
    "/music",
    responses={
        200: {
            "model": music_resp.MusicResponse,
            "description": "음악에 대한 정보를 반환합니다.",
        },
        404: {
            "description": "요청한 id는 존재하지 않는 id입니다.",
        },
    },
)
async def get_music_info(
    music_name: str = Query(..., description="음악 이름"),
    singer_name: str = Query(None, description="가수 이름"),
) -> JSONResponse:
    """요청한 음악에 대한 정보를 반환합니다.

    Args:
        music_name (str): 음악 이름.
        singer_name (str, optional): 가수 이름.

    Returns:
        JSONResponse:
            request_metadata (dict): 요청 정보
            response_metadata (dict): 응답 처리 정보
            music (Music): 음악과 음악 파일에 대한 정보
    """
    request_time = datetime.now()
    request_data = dict(music_name=music_name)
    if singer_name:
        request_data.update(dict(singer_name=singer_name))
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data=request_data,
    )

    # get music info from mongoDB
    fileDB = db.file
    musicDB = db.music

    music_data = musicDB.find_one(
        {
            "name": music_name,
            "singer": singer_name,
        }
    )
    file_data = fileDB.find_one({"_id": ObjectId(music_data["file_id"])})
    music = Music(
        file=file_data,
        **music_data,
    )

    response_time = datetime.now()
    response_metadata = ResponseMetadata(
        request_time=time2str(request_time),
        response_time=time2str(response_time),
        elapsed_time=elapsed(request_time, response_time),
    )
    response = music_resp.MusicResponse(
        request_metadata=request_metadata,
        response_metadata=response_metadata,
        music=music,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response),
    )


@router.get(
    "/musics",
    responses={
        200: {
            "model": music_resp.MusicChartResponse,
            "description": "음원 목록을 반환합니다.",
        },
        400: {
            "description": "조회하려는 데이터의 범위를 초과했습니다.",
        },
        404: {
            "description": "데이터가 존재하지 않습니다.",
        },
    },
)
async def serve_music_chart(
    limit: int = Query(10, description="불러올 차트의 개수")
) -> JSONResponse:
    """음원 차트를 반환합니다."""
    request_time = datetime.now()
    request_data = dict(limit=limit)

    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data=request_data,
    )

    # get music info from mongoDB
    fileDB = db.file
    musicDB = db.music
    musics = list()

    music_datas = musicDB.find()[:limit]
    for music_data in music_datas:
        file_data = fileDB.find_one({"_id": ObjectId(music_data["file_id"])})
        musics.append(
            Music(
                file=file_data,
                **music_data,
            )
        )

    response_time = datetime.now()
    response_metadata = ResponseMetadata(
        request_time=time2str(request_time),
        response_time=time2str(response_time),
        elapsed_time=elapsed(request_time, response_time),
    )
    response = music_resp.MusicChartResponse(
        request_metadata=request_metadata,
        response_metadata=response_metadata,
        musics=musics,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response),
    )
