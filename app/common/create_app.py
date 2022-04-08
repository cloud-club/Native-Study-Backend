from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import index, music, streaming


def create_app() -> FastAPI:
    app = FastAPI(
        title="CNP Music Streaming Service",
        version="0.2.0",
    )

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_methods=[],
        allow_headers=[],
    )

    # router
    app.include_router(
        index.router,
        tags=["status"],
    )
    app.include_router(
        streaming.router,
        prefix="/v1/api/streaming",
        tags=["streaming"],
    )
    app.include_router(
        music.router,
        prefix="/v1/api/musics",
        tags=["music"],
    )

    return app
