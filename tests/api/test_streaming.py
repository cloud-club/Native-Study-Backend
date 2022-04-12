import asyncio

import pyaudio
from httpx import AsyncClient

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5


async def send_request():
    url = "http://localhost/v1/api/streaming/?music_name=test"
    client = AsyncClient()
    async with client.stream("GET", url) as response:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK,
        )
        async for chunk in response.aiter_bytes():
            stream.write(chunk)
        stream.stop_stream()
        stream.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(send_request())
    loop.run_forever()
    loop.close()
