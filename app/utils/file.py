import mutagen
from starlette.datastructures import UploadFile

from app.common.type import Audio, t


class AudioFile:
    _file: Audio
    metadata: t.Dict
    content_type: str

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size: int):
        self.__size = size

    def __init__(self, file: UploadFile):
        content_type = file.content_type
        if not content_type.startswith("audio"):
            ext = content_type.split("/")[-1]
            raise ValueError(f"${ext} is not supported type")
        self.content_type = content_type
        self._file = mutagen.File(file.file)
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
        return dict(
            length=length,
            rate=sample_rate,
            channels=channels,
        )

    def _parse_wav_metadata(self) -> t.Dict:
        metadata = self._file.info
        length = metadata.length
        sample_rate = metadata.sample_rate
        channels = metadata.channels
        return dict(
            length=length,
            rate=sample_rate,
            channels=channels,
        )

    def save(self):
        pass
