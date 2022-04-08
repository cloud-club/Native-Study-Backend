from fastapi import APIRouter, Path, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.schema.response import music as music_resp

router = APIRouter()


@router.get(
    "/{music_id}",
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
        content=jsonable_encoder(music_resp.StreamMusicResponse),
    )
