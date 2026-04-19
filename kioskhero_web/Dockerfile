FROM python:3.14-slim-trixie AS buildcontainer

ARG DEBIAN_FRONTEND=noninteractiv

RUN apt-get update && apt-get install -y --no-install-recommends \
    optipng \
    jpegoptim \
    yui-compressor \
    libwebp-dev \
    libopenjp2-7-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libcairo2-dev \
    pkg-config \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy
# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=kioskhero_web/uv.lock,target=uv.lock \
    --mount=type=bind,source=kioskhero_web/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --directory=kioskhero_web


ENV DJANGO_SETTINGS_MODULE=kioskbear.conf.settings.production

ENV UV_NO_DEV=True
ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=secret,id=DJANGO_SECRET_KEY,env=DJANGO_SECRET_KEY \
    --mount=type=secret,id=MAILGUN_API_KEY,env=MAILGUN_API_KEY \
    uv run --directory=kioskhero_web django-admin collectstatic --noinput -i css/app.css

FROM python:3.14-slim-trixie

COPY --from=buildcontainer /app/ /app/
COPY --from=buildcontainer /usr/bin/optipng /usr/bin/optipng
COPY --from=buildcontainer /usr/bin/jpegoptim /usr/bin/jpegoptim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG DEBIAN_FRONTEND=noninteractiv
RUN apt-get update && apt-get install -y --no-install-recommends \
    htop \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/app/.venv \
    uv sync --frozen --no-dev --directory=kioskhero_web

EXPOSE 8000

RUN mkdir -p /app/logs/gunicorn

ENTRYPOINT ["uv", "run", "gunicorn", "kioskbear.conf.wsgi:application"]
