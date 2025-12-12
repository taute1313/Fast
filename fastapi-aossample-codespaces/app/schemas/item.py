from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(ge=0)
    tags: List[str] = []

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    tags: Optional[List[str]] = None

class Item(ItemBase):
    id: UUID = Field(default_factory=uuid4)
