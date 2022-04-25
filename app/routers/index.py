from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get(
    "/",
    responses={
        200: {"content": {"text": "pong"}, "description": "check server status",}
    },
)
def ping():
    return PlainTextResponse("pong")


@router.get(
    "/test",
    responses={
        200: {"content": {"text": "test"}, "description": "check server status",}
    },
)
def test_api():
    return PlainTextResponse("test api service")
