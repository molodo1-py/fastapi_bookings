import sys
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from os.path import abspath, dirname

# import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

sys.path.append(dirname(dirname(abspath(__file__))))

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import async_engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_importer
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router as router_users


#TODO: поменять библиотеку для версионирования и раскомментировать
# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
#     yield

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_importer)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
    allow_headers=[
        "Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin", "Authorization"
    ]
)

@app.get("/")
@version(1)
async def home() -> str:
    return 'API HOME'

app = VersionedFastAPI(app, prefix_format="/v{major}.{minor}")

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, async_engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.on_event("startup")
async def prepare_redis():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

#* для простого запуска 'python3 app/main.py'
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)