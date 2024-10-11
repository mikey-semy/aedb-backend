import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import auth, main, manuals, posts
from app.middlewares.docs_blocker import BlockDocsMiddleware
from app.const import (
    api_prefix,
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

app.include_router(auth.router, prefix=api_prefix)
app.include_router(posts.router, prefix=api_prefix)
app.include_router(main.router, prefix=api_prefix)
app.include_router(manuals.router, prefix=api_prefix)

app.add_middleware(BlockDocsMiddleware)
app.add_middleware(CORSMiddleware, **cors_params)

if __name__ == "__main__":
    uvicorn.run(app, **uvicorn_params)
