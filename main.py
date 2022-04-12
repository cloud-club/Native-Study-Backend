import uvicorn
from rich.traceback import install

install(show_locals=True)

from app.common.config import settings
from app.common.create_app import create_app

app = create_app()

reload = settings.APP_ENV != "production"


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=settings.MUSIC_SERVICE_INTERNAL_PORT,
        reload=reload,
    )
