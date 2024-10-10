"""
Основной модуль маршрутизации для приложения AEDB.

Этот модуль определяет маршруты для главной страницы, страницы документации
и страницы электробезопасности. Он использует шаблоны Jinja2 для рендеринга HTML-ответов.

Маршруты:
- /: Главная страница
- /manuals: Страница документации
- /es: Страница электробезопасности

Каждый маршрут возвращает HTML-ответ, используя соответствующий шаблон.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
 
from app.const import templates_path
from app.core.config import config

templates = Jinja2Templates(directory=str(templates_path))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    Обрабатывает запросы к главной странице.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: Отрендеренный HTML-ответ для главной страницы.
    """
    context = {
        "title": "AEDB",
        }
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context
    )

@router.middleware("http")
async def block_docs(request: Request, call_next):
    if not config.docs_access and request.url.path in ["/docs", "/redoc"]:
        return JSONResponse(status_code=403, content={"detail": "Access to documentation is forbidden."})
    response = await call_next(request)
    return response

@router.get("/instructions", response_class=HTMLResponse)
async def manuals(request: Request):
    """
    Обрабатывает запросы к странице документации.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: Отрендеренный HTML-ответ для страницы документации.
    """
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
    """
    Обрабатывает запросы к странице электробезопасности.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        TemplateResponse: Отрендеренный HTML-ответ для страницы электробезопасности.
    """
    context = {
        "title": "AEDB - Электробезопасность",
        }
    return templates.TemplateResponse(
        request=request,
        name="es.html",
        context=context
    )
