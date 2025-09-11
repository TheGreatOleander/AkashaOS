# AkashaOS Dockerfile - minimal, production-friendly
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip setuptools wheel || true
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

RUN groupadd -r akasha && useradd -r -g akasha akasha
RUN chown -R akasha:akasha /app
USER akasha

EXPOSE 8080
ENV FLASK_APP=tools/heartbeat/app.py
CMD ["python", "scripts/akasha_bootstrap.py"]
