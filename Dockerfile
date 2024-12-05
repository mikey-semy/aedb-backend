FROM python:3.12.3-alpine3.19

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && apk add --no-cache \
    postgresql-client \
    libpq \
    poppler-utils \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10 && \
    poetry install --no-dev --no-interaction --no-cache \
    && apk del .build-deps

EXPOSE 8000

COPY . /usr/src/app

COPY ./docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh
RUN chmod +x /usr/src/app/docker-entrypoint.sh

ENTRYPOINT ["sh", "/usr/src/app/docker-entrypoint.sh"]