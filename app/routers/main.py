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
