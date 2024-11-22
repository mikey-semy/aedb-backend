FROM python:3.12.1-alpine3.19

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apk update && apk add --no-cache postgresql-client build-base postgresql-dev libpq-dev poppler-utils
# RUN apk update && apk add postgresql-client build-base postgresql-dev libpq-dev poppler-utils
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && apk add --no-cache \
    postgresql-client \
    libpq \
    poppler-utils \
    && apk del .build-deps

RUN pip install --upgrade pip
COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
    
EXPOSE 8000

COPY . /usr/src/app

# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
# USER appuser

COPY ./docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh
RUN chmod +x /usr/src/app/docker-entrypoint.sh

ENTRYPOINT ["sh", "/usr/src/app/docker-entrypoint.sh"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
