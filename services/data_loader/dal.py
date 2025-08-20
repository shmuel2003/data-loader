import os
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ASCENDING

from models import Soldier, SoldierUpdate

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "enemy_soldiers")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "soldier_details")

class SoldierDAL:
    def __init__(self,
            mongo_uri: str = MONGODB_URI,
            db_name: str = DB_NAME,
            collection_name: str = COLLECTION_NAME):
        self._mongo_uri = mongo_uri
        self._db_name = db_name
        self._collection_name = collection_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._col: Optional[AsyncIOMotorCollection] = None

    async def connect(self) -> None:
        self._client = AsyncIOMotorClient(self._mongo_uri)
        db = self._client[self._db_name]
        self._col = db[self._collection_name]
        # Ensure unique index on `id`
        await self._col.create_index([("id", ASCENDING)], unique=True, name="uniq_id")

    async def close(self) -> None:
        if self._client:
            self._client.close()

    # CRUD
    async def get_all(self) -> List[Dict[str, Any]]:
        cursor = self._col.find({}, {"_id": 0})
        return [doc async for doc in cursor]

    async def get_by_id(self, soldier_id: int) -> Optional[Dict[str, Any]]:
        return await self._col.find_one({"id": soldier_id}, {"_id": 0})

    async def create(self, soldier: Soldier) -> bool:
        doc = soldier.model_dump()
        result = await self._col.insert_one(doc)
        return result.acknowledged

    async def update(self, soldier_id: int, changes: SoldierUpdate) -> bool:
        payload = {k: v for k, v in changes.model_dump(exclude_unset=True).items() if v is not None}
        if not payload:
            return False
        result = await self._col.update_one({"id": soldier_id}, {"$set": payload})
        return result.matched_count == 1

    async def delete(self, soldier_id: int) -> bool:
        result = await self._col.delete_one({"id": soldier_id})
        return result.deleted_count == 1