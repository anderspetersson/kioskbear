FROM eu.gcr.io/roiiogcloud/python:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    optipng \
    jpegoptim \
    yui-compressor \
    libwebp-dev \
    libopenjp2-7-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

# Install requirements.
# Use no-cache-dir to save disk space since
# the docker image will be cached anyway.
ADD requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ADD . /app
RUN pip3 install -e /app/
RUN npm install
RUN npm run build

ENV DJANGO_SETTINGS_MODULE=kioskbear.conf.settings.production

RUN django-admin collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "kioskbear.conf.wsgi:application"]
