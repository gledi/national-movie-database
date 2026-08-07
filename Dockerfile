# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends libpq5 && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes --purge && \
    DEBIAN_FRONTEND=noninteractive apt-get autoclean --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get clean --yes && \
    rm -rf /var/lib/apt/lists/* && \
    useradd --system --user-group --no-create-home --shell /sbin/nologin nmdb


FROM python:${PYTHON_VERSION}-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends libpq-dev && \
    DEBIAN_FRONTEND=noninteractive apt-get autoremove --yes --purge && \
    DEBIAN_FRONTEND=noninteractive apt-get autoclean --yes && \
    DEBIAN_FRONTEND=noninteractive apt-get clean --yes && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./


FROM builder AS dev-builder
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --all-extras --all-groups
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --all-extras --all-groups


FROM builder AS prod-builder
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --extra=prod --no-dev
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --extra=prod --no-dev


FROM base AS dev
COPY --from=dev-builder /app /app
ENV PATH="/app/.venv/bin:$PATH"


FROM base AS prod
COPY --from=prod-builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=nmdb.core.settings.production
USER nmdb
CMD ["daphne", "--no-server-name", "--bind", "0.0.0.0", "--port", "8000", "nmdb.core.asgi:application"]
