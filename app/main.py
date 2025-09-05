from fastapi import FastAPI

from app.routers import health, parse

app = FastAPI(version="0.0.1", title="open-parse-api")

api_prefix = "/api"
app.include_router(health.router, prefix=api_prefix)
app.include_router(parse.router, prefix=api_prefix)
