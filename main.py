from os import environ

import uvicorn
from fastapi import FastAPI, Form, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, PlainTextResponse

from app.schema.response import music as music_resp

app = FastAPI(
    title="CNP Music Streaming Service",
    version="0.2.0",
)

APP_ENV = environ.get("APP_ENV", "dev")
reload = APP_ENV != "production"


@app.get("/")
def ping():
    return PlainTextResponse("pong")


@app.post(
    "/v1/api/musics",
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
    music_file: UploadFile = Form(...),
) -> JSONResponse:
    """음악 파일과 음악 메타정보를 저장 합니다."""
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=music_resp.UploadMusicResponse,
    )


@app.get(
    "/v1/api/musics/{music_id}",
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
        content=music_resp.MusicResponse,
    )


@app.get(
    "/v1/api/musics",
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
        content=music_resp.MusicChartResponse,
    )


@app.get(
    "/v1/api/streaming/{music_id}",
    responses={
        200: {"model": music_resp.StreamMusicResponse, "description": "요청한 음악을 스트리밍"},
    },
)
async def stream_music(
    music_id: str = Path(..., description="음원 고유 아이디"),
) -> JSONResponse:
    """요청한 음악을 스트리밍합니다."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=music_resp.StreamMusicResponse,
    )


if __name__ == "__main__":

    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
        reload=reload,
    )
