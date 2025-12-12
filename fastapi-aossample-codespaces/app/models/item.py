from uuid import UUID
from pydantic import BaseModel

class ItemModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    price: float
    tags: list[str] = []
