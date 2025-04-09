# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.12-slim

# Install system dependencies
RUN apt update \
    && apt install -y --no-install-recommends python3-dev build-essential libpq-dev dos2unix \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install "poetry==2.1.1"

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

RUN rm -rf .dockerignore \
  LICENSE \
  poetry.lock \
  poetry.toml \
  README.md

EXPOSE 8000
CMD ["python", "run.py"]