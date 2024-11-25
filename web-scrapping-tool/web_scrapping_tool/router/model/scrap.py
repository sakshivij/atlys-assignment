from pydantic import BaseModel


class ScrapCreate(BaseModel):
    data: dict

class Scrap(BaseModel):
    id: str
    request_id: str
    data: dict

    class Config:
        orm_mode = True
