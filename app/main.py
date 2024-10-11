import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.docs_blocker import BlockDocsMiddleware
from app.const import (
    api_prefix,
    routers,
    app_params,
    uvicorn_params,
    static_params,
    media_params
)
from app.version import __version__
from app.core.config import cors_params

app = FastAPI(**app_params)

app.mount(**static_params)
app.mount(**media_params)

for router in routers:
    app.include_router(router.router, prefix=api_prefix)

app.add_middleware(BlockDocsMiddleware)
app.add_middleware(CORSMiddleware, **cors_params)

if __name__ == "__main__":
    uvicorn.run(app, **uvicorn_params)
