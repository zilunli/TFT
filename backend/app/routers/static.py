from fastapi import APIRouter
from app.services.riot import get_champions, get_items, get_traits, get_augments, get_queue_type_by_queue_id, get_tactician_by_companion_item_id

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

@router.get("/queue-types/{queue_id}")
async def queue_type_by_queue_id(queue_id):
    return await get_queue_type_by_queue_id(queue_id)

@router.get("/tacticians/{item_id}")
async def tactician_by_companion_item_id(item_id):
    return await get_tactician_by_companion_item_id(item_id) 