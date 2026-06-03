from fastapi import APIRouter
from database import settings_col

router = APIRouter()

@router.get("/")
async def get_settings():
    s = await settings_col.find_one({}, {"_id": 0})
    return s or {}

@router.put("/")
async def update_settings(updates: dict):
    await settings_col.update_one({}, {"$set": updates}, upsert=True)
    return {"success": True}

@router.post("/seed")
async def seed_settings():
    # Call this once after deploy to push default data into Atlas
    from database import teachers_col, quizzes_col, announcements_col, students_col
    # insert your DEFAULT_TEACHERS, DEFAULT_QUIZZES etc here
    return {"seeded": True}