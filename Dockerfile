FROM python:3.6-alpine
RUN apk add --no-cache --virtual .build-deps \
    git \
    g++ \
    libmagic \
    make
COPY ./requirements.pip /app/requirements.pip
RUN pip install --no-cache-dir --upgrade pip setuptools \
  && pip install --no-cache-dir -r /app/requirements.pip
COPY . /app
WORKDIR /app
RUN pip install -e .