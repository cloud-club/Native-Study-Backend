import typing as t

from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: t.Any):
        if not isinstance(v, BsonObjectId):
            raise TypeError("bson ObjectId required")
        return str(v)
