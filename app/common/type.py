import typing as t
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

PathStr = t.Union[Path, str]
Audio = t.Union[MP3, WAVE]
