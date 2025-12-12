from typing import Dict, List
from uuid import UUID
from app.schemas.item import Item, ItemCreate, ItemUpdate

class ItemsRepository:
    def __init__(self):
        self._items: Dict[UUID, Item] = {}

    def list(self, skip: int = 0, limit: int = 50) -> List[Item]:
        values = list(self._items.values())
        return values[skip : skip + limit]

    def get(self, item_id: UUID) -> Item | None:
        return self._items.get(item_id)

    def create(self, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        self._items[item.id] = item
        return item

    def replace(self, item_id: UUID, data: Item) -> Item:
        self._items[item_id] = data
        return data

    def update(self, item_id: UUID, data: ItemUpdate) -> Item | None:
        current = self._items.get(item_id)
        if not current:
            return None
        updated = current.model_copy(update={k: v for k, v in data.model_dump(exclude_unset=True).items()})
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: UUID) -> bool:
        return self._items.pop(item_id, None) is not None

repo = ItemsRepository()
