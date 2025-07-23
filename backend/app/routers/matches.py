from fastapi import APIRouter
from app.services.riot import get_history_by_puuid, get_match_by_match_id

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/history/{puuid}")
async def history(puuid: str, start: int = 0, count: int = 20):
    return await get_history_by_puuid(puuid, start, count)

@router.get("/{match_id}")
async def match(match_id: str):
    return await get_match_by_match_id(match_id)
