import typing as t
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel

request_time = datetime.now()
response_time = datetime.now()
elapsed_time = (response_time - request_time).total_seconds() * 1000
request_time_str = request_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
response_time_str = response_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

response_metadata = {
    "request_time": request_time_str,
    "response_time": response_time_str,
    "elapsed_time": elapsed_time,
}


class ResponseMetadata(BaseModel):
    request_time: str
    response_time: str
    elapsed_time: float

    class Config:
        schema_extra = {
            "example": response_metadata,
        }


class RequestMetadata(BaseModel):
    request_id: str
    request_data: t.Dict

    class Config:
        schema_extra = {
            "example": {
                "request_id": str(uuid4()),
                "request_data": dict(),
            },
        }


class BaseResponse(BaseModel):
    request_metadata: RequestMetadata
    response_metadata: ResponseMetadata
