from fastapi import APIRouter
from app.services.riot import get_champions, get_items, get_traits, get_augments

router = APIRouter(prefix="/static", tags=["static"])

@router.get("/champions")
async def champions():
    return await get_champions()

@router.get("/items")
async def items():
    return await get_items()

@router.get("/traits")
async def traits():
    return await get_traits()

@router.get("/augments")
async def augments():
    return await get_augments()
