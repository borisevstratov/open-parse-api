# open-parse-api

A lightweight REST API wrapper for [open-parse](https://github.com/Filimoa/open-parse).
Makes it easy to run open-parse as a standalone service.

Feel free to fork and adjust it to your own scenarios!

## Local setup

### Requirements

- Python 3.12 or higher.
- `uv` package manager. [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

1. Install Tesseract. [Installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html)
2. Install project dependencies using `uv`

```bash
uv sync
```

3. Run the application

```bash
uv run fastapi dev
```

The application will be available at <http://localhost:8000>

Swagger docs: <http://localhost:8000/docs>

## API

### Parse a Document

**POST** `/api/parse/basic`

- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file`: The PDF document to parse

#### Example

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/api/parse/basic
```

## Customization

- **Pipelines**
Feel free to fork and adjust routes, pipelines and other config in to fit your use case.
You can modify extraction rules, pipelines, or table parsing algorithms.
  - Pipelines: [app/utils/parser.py](app/utils/parser.py)
  - Routes: [app/routers/parse.py](app/routers/parse.py)

- **OCR Languages**
English (`tesseract-ocr-eng`) is installed by default.
To add more languages, extend the [Dockerfile](Dockerfile)

```Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    libtesseract-dev \
    tesseract-ocr-eng \
    tesseract-ocr-fra \   # French
    tesseract-ocr-deu \   # German
    tesseract-ocr-spa \   # Spanish
    && rm -rf /var/lib/apt/lists/*
```

## Going for production

This project is fully containerized and can be built with Docker

### Build and Run Locally

```bash
# Build the image
docker build -t open-parse-api .

# Run the container
docker run -p 8000:8000 open-parse-api
```

Usage with Docker Compose

```yaml
services:
  open-parse-api:
    # Local image
    image: open-parse-api:latest
    # Published image
    # image: ghcr.io/<your-username-or-org>/open-parse-api:latest
    container_name: open-parse-api
    restart: unless-stopped
    ports:
      - "8000:8000"
```

### CI/CD

This repository includes a GitHub Action [.github/workflows/build.yml](.github/workflows/build.yml) that automatically builds and pushes the Docker image on every push to `master` branch to `ghcr.io<your-username-or-org>open-parse-api`
