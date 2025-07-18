from fastapi import APIRouter
from app.services.riot import get_summoner_by_puuid

router = APIRouter(prefix="/summoners", tags=["summoners"])

@router.get("/{puuid}")
async def summoner(puuid: str):
    return await get_summoner_by_puuid(puuid)
