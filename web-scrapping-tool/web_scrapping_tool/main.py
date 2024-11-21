import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import EnvironmentVariables
from .router.setting import router as setting_router
from .router.user import router as user_router

app = FastAPI(
    docs_url='/api/1/swagger/index.html',
    openapi_url='/openapi.json',
    title='Web Scrapper API',
    description="API to scrap data from websites",
    version='1.0.0',
)
env = EnvironmentVariables()

origins = env.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=['User'])
app.include_router(setting_router, tags=['Setting'])

if __name__ == "__main__":
    uvicorn.run(app, host=env.host, port=env.port)
