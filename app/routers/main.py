from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.const import templates_path

templates = Jinja2Templates(directory=str(templates_path))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    context = {
        "title": "AEDB",
        }
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context
    )

@router.get("/manuals", response_class=HTMLResponse)
async def manuals(request: Request):
    context = {
        "title": "AEDB - Документация",
        }
    return templates.TemplateResponse(
        request=request,
        name="manuals.html",
        context=context
    )

@router.get("/es", response_class=HTMLResponse)
async def es(request: Request):
    context = {
        "title": "AEDB - Электробезопасность",
        }
    return templates.TemplateResponse(
        request=request,
        name="es.html",
        context=context
    )
