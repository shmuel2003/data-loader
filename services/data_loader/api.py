import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from dal import SoldierDAL
from models import Soldier, SoldierUpdate

app = FastAPI(title="Enemy Soldiers CRUD API",
                version="1.0.0",
                openapi_url="/openapi.json")

# DAL singleton for app lifetime
soldier_dal = SoldierDAL()

@app.on_event("startup")
async def on_startup():
    await soldier_dal.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await soldier_dal.close()

# Dependency (kept simple for future DI)
async def get_dal() -> SoldierDAL:
    return soldier_dal

BASE = "/soldiersdb"

@app.get(f"{BASE}/", response_model=List[Soldier])
async def list_soldiers(dal: SoldierDAL = Depends(get_dal)):
    return await dal.get_all()

@app.get(f"{BASE}/{{soldier_id}}", response_model=Soldier)
async def fetch_soldier(soldier_id: int, dal: SoldierDAL = Depends(get_dal)):
    doc = await dal.get_by_id(soldier_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Soldier not found")
    return doc

@app.post(f"{BASE}/", status_code=201)
async def create_soldier(soldier: Soldier, dal: SoldierDAL = Depends(get_dal)):
    try:
        ok = await dal.create(soldier)
        if not ok:
            raise HTTPException(status_code=500, detail="Insert not acknowledged")
    except Exception as e:
        # likely duplicate key error or validation
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse({"status": "created"}, status_code=201)

@app.put(f"{BASE}/{{soldier_id}}")
async def update_soldier(soldier_id: int, changes: SoldierUpdate, dal: SoldierDAL = Depends(get_dal)):
    ok = await dal.update(soldier_id, changes)
    if not ok:
        raise HTTPException(status_code=404, detail="Soldier not found or no changes provided")
    return {"status": "updated"}

@app.delete(f"{BASE}/{{soldier_id}}")
async def delete_soldier(soldier_id: int, dal: SoldierDAL = Depends(get_dal)):
    ok = await dal.delete(soldier_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Soldier not found")
    return {"status": "deleted"}

if __name__ == "__main__":
    uvicorn.run("services.data_loader.api:app", host="0.0.0.0", port=8000, reload=True)