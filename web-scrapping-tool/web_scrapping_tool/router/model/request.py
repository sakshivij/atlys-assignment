from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class Status(Enum):
    UNPROCESSED = "unprocessed"
    PENDING = "pending"
    PROCESSED = "processed"

class RequestCreate(BaseModel):
    override_page_limit: Optional[int]
    setting_id: str
    name: str
    status: Status


class Request(BaseModel):
    id: str
    override_page_limit: Optional[int]
    setting_id: str
    name: str

    class Config:
        orm_mode = True
