# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12.1-alpine3.19

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add postgresql-client build-base postgresql-dev libpq-dev

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION="1.8.3"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/venv/bin:${PATH}"

COPY poetry.* pyproject.toml ./
RUN poetry install --no-dev
    

WORKDIR /usr/src/app
COPY . /usr/src/app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
USER appuser

COPY ./docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh
RUN chmod +x /usr/src/app/docker-entrypoint.sh

ENTRYPOINT ["sh", "/usr/src/app/docker-entrypoint.sh"]
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
