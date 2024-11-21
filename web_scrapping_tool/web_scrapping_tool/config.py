import json
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentVariables(BaseSettings):
    port: int = Field(8000, env='PORT')
    database_url: str = Field(..., env='DATABASE_URL')
    host: str = Field(..., env='HOST')
    origins: str = Field(..., env='ORIGINS')
    database: str = Field("main", env="DATABASE")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
