FROM python:3.11-bullseye as builder

COPY ./requirements/ /requirements/

ARG ENVIRONMENT=dev

RUN apt-get update \
    && apt-get --yes upgrade \
    && python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels --requirement=/requirements/${ENVIRONMENT}.txt


FROM python:3.11-slim-bullseye as final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /wheels/ /wheels/
COPY --from=builder /requirements/ /requirements/

ARG ENVIRONMENT=dev

RUN apt-get update \
    && apt-get --yes upgrade \
    && apt-get --yes install --no-install-recommends libpq5 wait-for-it \
    && python -m pip install --no-cache-dir --upgrade pip setuptools wheel debugpy \
    && python -m pip install --no-cache-dir --no-index --find-links=/wheels --requirement=/requirements/${ENVIRONMENT}.txt \
    && apt-get --yes autoremove \
    && apt-get --yes autoclean \
    && apt-get --yes clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /wheels /requirements
