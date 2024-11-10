"""
Основной модуль маршрутизации для приложения AEDB.

Этот модуль определяет маршруты для главной страницы. 
Он использует шаблоны Jinja2 для рендеринга HTML-ответов.

Маршруты:
- /: Главная страница

Каждый маршрут возвращает HTML-ответ, используя соответствующий шаблон.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.const import main_params, templates_path

templates = Jinja2Templates(directory=str(templates_path))

router = APIRouter(**main_params)

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
