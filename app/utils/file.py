from io import BytesIO

import mutagen
from starlette.datastructures import UploadFile

from app.common.type import Audio, t
from app.database.storage import storage


class AudioFile:
    _file: Audio
    binary: UploadFile
    metadata: t.Dict
    content_type: str
    size: int

    def __init__(self, file: bytes, content_type: str):
        if not content_type.startswith("audio"):
            ext = content_type.split("/")[-1]
            raise ValueError(f"${ext} is not supported type")
        self.size = len(file)
        self.binary = BytesIO(file)
        self.content_type = content_type
        self._file = mutagen.File(BytesIO(file))
        self.metadata = self.parse_metadata()

    def parse_metadata(self):
        parser = None
        if self.content_type.endswith("wav"):
            parser = self._parse_mp3_metadata
        elif self.content_type.endswith("mp3"):
            parser = self._parse_wav_metadata
        return parser()

    def _parse_mp3_metadata(self) -> t.Dict:
        metadata = self._file.info
        length = metadata.length
        sample_rate = metadata.sample_rate
        channels = metadata.channels
        return dict(length=length, rate=sample_rate, channels=channels, size=self.size,)

    def _parse_wav_metadata(self) -> t.Dict:
        metadata = self._file.info
        length = metadata.length
        sample_rate = metadata.sample_rate
        channels = metadata.channels
        return dict(length=length, rate=sample_rate, channels=channels, size=self.size,)

    async def save(self, filename: str, bucket_name: str = "music") -> str:
        result = storage.save(
            bucket_name=bucket_name,
            object_name=filename,
            binary=self.binary,
            length=self.size,
        )
        if not result:
            raise ValueError
        return f"/{bucket_name}/{filename}"
