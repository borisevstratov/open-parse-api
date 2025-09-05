from datetime import datetime
from fastapi import APIRouter

router = APIRouter(tags=["health"], prefix="/health")


@router.get("/")
def health():
    return {
        "service": "open-parse-api",
        "message": "success",
        "time": datetime.now(),
    }
