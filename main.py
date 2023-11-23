from fastapi import FastAPI

from api.router import router

app = FastAPI(
    title="SpaceX Trello API",
    version="0.0.1",
)

app.include_router(router)
