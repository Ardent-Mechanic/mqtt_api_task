from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from db import db_session
from model import Base
from utils.mqtt_client_test import fast_mqtt
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await fast_mqtt.mqtt_startup()
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await fast_mqtt.mqtt_shutdown()
        await db_session.dispose()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
