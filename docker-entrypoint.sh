#!/usr/bin/bash
echo "Запуск скрипта docker-entrypoint.sh"
echo "Применение миграции"
alembic upgrade head
echo "Запуск сервера uvicorn"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers