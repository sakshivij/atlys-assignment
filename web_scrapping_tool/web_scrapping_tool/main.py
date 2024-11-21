import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import EnvironmentVariables
from .router.user import router as user_router

app = FastAPI()
env = EnvironmentVariables()

origins = env.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host=env.host, port=env.port)
