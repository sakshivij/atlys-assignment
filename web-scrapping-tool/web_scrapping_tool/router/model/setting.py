from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class SettingCreate(BaseModel):
    is_scrapping_paginated: bool
    is_page_query_parameter: bool
    max_pages_limit: int
    proxy: Optional[str] = Query("", description="Proxy in the format http://user:password@proxyserver:port")
    name: Optional[str]
    base_url: str

class Setting(BaseModel):
    id: str
    is_scrapping_paginated: bool
    is_page_query_parameter: bool
    max_pages_limit: int
    name: Optional[str]
    proxy: Optional[str] = Query(None, description="Proxy in the format http://user:password@proxyserver:port")
    base_url: str

    class Config:
        orm_mode = True
