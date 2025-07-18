from fastapi import APIRouter
from app.services.riot import get_match_history, get_match_detail

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/matches/history/")
async def match_history(puuid: str, start: int = 0, count: int = 20):
    return await get_match_history(puuid, start, count)

@router.get("/matches/details/")
async def match_detail(match_id: str):
    return await get_match_detail(match_id)
