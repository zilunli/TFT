from fastapi import APIRouter
from app.services.riot import get_account_by_gamename_and_tagline

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/{gameName}/{tagLine}")
async def account(gameName: str, tagLine: str):
    return await get_account_by_gamename_and_tagline(gameName, tagLine)
