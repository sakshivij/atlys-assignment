import json
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentVariables(BaseSettings):
    port: int = Field(8000, env='PORT')
    database_url: str = Field("mongodb://foobar:foobar@docker-mongo:27017", env='DATABASE_URL')
    host: str = Field("127.0.0.1", env='HOST')
    origins: str = Field("http://localhost:8080", env='ORIGINS')
    database: str = Field("main", env="DATABASE")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
