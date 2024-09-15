import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.const import app_params, uvicorn_params, static_params, media_params
from app.core.config import cors_params
from app.routers import main, manuals

app = FastAPI(**app_params)

app.mount(**static_params)
app.mount(**media_params)

app.include_router(main.router)
app.include_router(manuals.router)

app.add_middleware(CORSMiddleware, **cors_params)

if __name__ == "__main__":
    uvicorn.run(app, **uvicorn_params)
