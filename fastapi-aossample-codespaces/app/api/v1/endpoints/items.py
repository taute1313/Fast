from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.repositories.items_repo import repo

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 50):
    return repo.list(skip=skip, limit=limit)

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate):
    return repo.create(payload)

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: UUID):
    item = repo.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def replace_item(item_id: UUID, payload: Item):
    if item_id != payload.id:
        raise HTTPException(status_code=400, detail="Path id and body id mismatch")
    return repo.replace(item_id, payload)

@router.patch("/{item_id}", response_model=Item)
async def update_item(item_id: UUID, payload: ItemUpdate):
    updated = repo.update(item_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID):
    deleted = repo.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
