# Builder stage
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libtesseract-dev \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

COPY . .

# Runtime stage
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libtesseract-dev \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app /app

CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
