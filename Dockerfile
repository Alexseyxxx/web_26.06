FROM python:3.13.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y\
    libpq-dev build-essential

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh