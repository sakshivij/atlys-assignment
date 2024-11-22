from enum import Enum
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, validator


class Status(Enum):
    UNPROCESSED = "unprocessed"
    PENDING = "pending"
    PROCESSED = "processed"

class KeyMapper(BaseModel):
    field_name: str
    mapped_to: str
    requires_fetch: Optional[bool] = False
    attribute_name: Optional[str] = ""

class ScrapMetaInformation(BaseModel):
    root_selector: str
    field_mappings: List[KeyMapper]
    is_multiple_items: bool    

# TODO: Why these not being picked as optional
class RequestCreate(BaseModel):
    override_page_limit: Optional[int]
    setting_id: str
    name: str
    status: Status
    meta: ScrapMetaInformation

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if isinstance(data.get('status'), Status):
            data['status'] = data['status'].value
        return data

    @validator('status', pre=True)
    def parse_status(cls, value):
        if isinstance(value, str):
            return Status(value)
        return value


class Request(BaseModel):
    id: str
    override_page_limit: Optional[int]
    setting_id: str
    name: str
    status: Status
    meta: ScrapMetaInformation

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if isinstance(data.get('status'), Status):
            data['status'] = data['status'].value
        return data
    
    @validator('status', pre=True)
    def parse_status(cls, value):
        if isinstance(value, str):
            return Status(value)  # Convert string to Enum
        return value
    class Config:
        orm_mode = True
        use_enum_values = True
