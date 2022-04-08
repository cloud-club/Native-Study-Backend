from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, File, Form, Path, Query, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.schema.response import music as music_resp
from app.schema.response.common import RequestMetadata, ResponseMetadata
from app.utils.time import elapsed, time2str

router = APIRouter()


@router.post(
    "/",
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
    """음악 파일과 음악 메타정보를 저장 합니다."""
    request_time = datetime.now()
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data={
            "music_id": 112453,
            "music_name": music_name,
            "singer_name": singer_name,
            "release_date": release_date,
            "play_total": 128,
            "music_file": music_file.filename,
        },
    )

    # @TODO: file validation
    # @TODO: save file in minIO
    # @TODO: save data in DB

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
    "/{music_id}",
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
    music_id: str = Path(..., description="음원 고유 아이디"),
) -> JSONResponse:
    """요청한 음악에 대한 정보를 반환합니다."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(music_resp.MusicResponse),
    )


@router.get(
    "/",
    responses={
        200: {
            "model": music_resp.MusicChartResponse,
            "description": "음원 목록을 반환합니다.",
        },
        400: {
            "description": "올바른 형태의 offset이 아닙니다.",
        },
        404: {
            "description": "offset이 범위를 벗어났습니다.",
        },
    },
)
async def serve_music_chart(
    offset: str = Query(None, description="불러올 차트의 오프셋 [0 = no limit] e.g.)1-2,5")
) -> JSONResponse:
    """음원 차트를 반환합니다."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(music_resp.MusicChartResponse),
    )
