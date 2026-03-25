FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app
COPY main.py pyproject.toml uv.lock crontab .

ENV UV_NO_DEV=1

RUN uv sync
RUN crontab crontab

CMD ["crond", "-f"]