from pydantic import BaseModel, Field
from typing import Optional

class Soldier(BaseModel):
    """Represents a soldier document for the enemy_soldiers DB.

    We keep an explicit numeric `id` that is unique in the collection.
    MongoDB's native `_id` is still present (ObjectId) but not exposed in the API.
    """

    id: int = Field(..., description="Unique numeric ID")
    first_name: str
    last_name: str
    phone_number: str
    rank: str

class SoldierUpdate(BaseModel):
    """Partial update model (all fields optional)."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    rank: Optional[str] = None