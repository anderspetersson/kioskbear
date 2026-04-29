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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app/kioskbear_web

ENV DJANGO_SETTINGS_MODULE=kioskbear.conf.settings.production

ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=secret,id=DJANGO_SECRET_KEY,env=DJANGO_SECRET_KEY \
    --mount=type=secret,id=MAILGUN_API_KEY,env=MAILGUN_API_KEY \
    uv run django-admin collectstatic --noinput -i css/app.css

RUN --mount=type=cache,target=/app/.venv \
    uv sync --no-dev

RUN mkdir -p /app/logs/gunicorn

ENTRYPOINT ["uv", "run", "gunicorn", "kioskbear.conf.wsgi:application"]
