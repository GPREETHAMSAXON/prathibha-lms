from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
import random
import string
from database import announcements_col

router = APIRouter()


# --- PYDANTIC MODELS ---

class Announcement(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    createdBy: str              # "Principal (Admin)" or teacher name
    date: Optional[str] = None  # auto-set to today if not provided
    classNum: str               # "All" or specific class e.g. "10", "8"


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    classNum: Optional[str] = None


# --- HELPER ---

def generate_id():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"a_{suffix}"


# --- ROUTES ---

# GET all announcements (sorted newest first)
@router.get("/")
async def get_all_announcements():
    announcements = await announcements_col.find(
        {},
        {"_id": 0}
    ).sort("date", -1).to_list(None)
    return announcements


# GET announcements for a specific class
# Returns both class-specific AND school-wide ("All") announcements
@router.get("/class/{class_num}")
async def get_announcements_for_class(class_num: str):
    announcements = await announcements_col.find(
        {"$or": [{"classNum": class_num}, {"classNum": "All"}]},
        {"_id": 0}
    ).sort("date", -1).to_list(None)
    return announcements


# GET school-wide announcements only
@router.get("/school-wide")
async def get_school_wide_announcements():
    announcements = await announcements_col.find(
        {"classNum": "All"},
        {"_id": 0}
    ).sort("date", -1).to_list(None)
    return announcements


# GET single announcement by ID
@router.get("/{announcement_id}")
async def get_announcement(announcement_id: str):
    announcement = await announcements_col.find_one(
        {"id": announcement_id},
        {"_id": 0}
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement


# POST create a new announcement (principal or teacher)
@router.post("/")
async def create_announcement(announcement: Announcement):
    doc = announcement.dict()

    if not doc["id"]:
        doc["id"] = generate_id()

    # Auto-set date to today if not provided
    if not doc["date"]:
        doc["date"] = str(date.today())

    # Validate classNum — must be "All" or a valid class 1–10
    valid_classes = {"All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
    if doc["classNum"] not in valid_classes:
        raise HTTPException(
            status_code=400,
            detail=f"classNum must be 'All' or a class number between 1 and 10"
        )

    await announcements_col.insert_one(doc)
    return {"success": True, "announcementId": doc["id"]}


# PUT update an announcement (only title, description, classNum can change)
@router.put("/{announcement_id}")
async def update_announcement(announcement_id: str, updates: AnnouncementUpdate):
    existing = await announcements_col.find_one({"id": announcement_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Announcement not found")

    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # Validate classNum if it's being updated
    if "classNum" in update_data:
        valid_classes = {"All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
        if update_data["classNum"] not in valid_classes:
            raise HTTPException(
                status_code=400,
                detail="classNum must be 'All' or a class number between 1 and 10"
            )

    await announcements_col.update_one({"id": announcement_id}, {"$set": update_data})
    return {"success": True}


# DELETE an announcement
@router.delete("/{announcement_id}")
async def delete_announcement(announcement_id: str):
    result = await announcements_col.delete_one({"id": announcement_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"success": True}