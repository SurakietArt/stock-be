ARG PYTHON_VERSION="3.12"
FROM python:${PYTHON_VERSION}-slim

ENV POETRY_VERSION="2.1.3" \
    POETRY_NO_INTERACTION=1 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl build-essential libpq-dev cron tzdata \
 && ln -snf /usr/share/zoneinfo/Asia/Bangkok /etc/localtime \
 && echo "Asia/Bangkok" > /etc/timezone \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false \
 && poetry install --no-ansi --with deployment,main

ARG EXPOSE_PORT=8080
ENV EXPOSE_PORT=$EXPOSE_PORT \
    WORKER_TIMEOUT=300 \
    WORKER_GRACEFUL_TIMEOUT=90 \
    WORKER_SPAWN=3 \
    THREADS_SPAWN=2 \
    HTTP_KEEP_ALIVE=5 \
    MAX_REQUEST_WORKER_RESTART=100 \
    MAX_REQUEST_WORKER_JITTER=10

EXPOSE $EXPOSE_PORT

COPY . .
RUN python manage.py collectstatic --noinput

CMD python manage.py migrate && gunicorn \
    --worker-class=gthread \
    --threads ${THREADS_SPAWN} \
    --workers ${WORKER_SPAWN} \
    --bind 0.0.0.0:${EXPOSE_PORT} \
    --timeout ${WORKER_TIMEOUT} \
    --graceful-timeout ${WORKER_GRACEFUL_TIMEOUT} \
    --keep-alive ${HTTP_KEEP_ALIVE} \
    --max-requests ${MAX_REQUEST_WORKER_RESTART} \
    --max-requests-jitter ${MAX_REQUEST_WORKER_JITTER} \
    --preload \
    stock_be.wsgi
