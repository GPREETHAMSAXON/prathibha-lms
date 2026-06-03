from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
import random
import string
from database import feedback_col

router = APIRouter()


# --- PYDANTIC MODELS ---

class Feedback(BaseModel):
    id: Optional[str] = None
    name: str                       # parent or student name
    classNum: str                   # class of the student
    email: str                      # parent/student email
    message: str
    date: Optional[str] = None      # auto-set to today if not provided


# --- HELPER ---

def generate_id():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"f_{suffix}"


# --- ROUTES ---

# GET all feedback (principal only)
@router.get("/")
async def get_all_feedback():
    feedback_list = await feedback_col.find({}, {"_id": 0}).sort("date", -1).to_list(None)
    return feedback_list


# GET feedback filtered by class (principal view)
@router.get("/class/{class_num}")
async def get_feedback_by_class(class_num: str):
    feedback_list = await feedback_col.find(
        {"classNum": class_num},
        {"_id": 0}
    ).sort("date", -1).to_list(None)
    return feedback_list


# GET single feedback entry by ID
@router.get("/{feedback_id}")
async def get_feedback(feedback_id: str):
    feedback = await feedback_col.find_one({"id": feedback_id}, {"_id": 0})
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback entry not found")
    return feedback


# POST submit new feedback (public — any parent or student can submit)
@router.post("/")
async def submit_feedback(feedback: Feedback):
    # Basic message length validation
    if len(feedback.message.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Feedback message must be at least 10 characters long"
        )
    if len(feedback.message.strip()) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Feedback message cannot exceed 1000 characters"
        )

    # Validate classNum
    valid_classes = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
    if feedback.classNum not in valid_classes:
        raise HTTPException(
            status_code=400,
            detail="classNum must be a class number between 1 and 10"
        )

    doc = feedback.dict()
    if not doc["id"]:
        doc["id"] = generate_id()

    # Auto-set date to today if not provided
    if not doc["date"]:
        doc["date"] = str(date.today())

    doc["email"] = doc["email"].lower().strip()
    doc["message"] = doc["message"].strip()

    await feedback_col.insert_one(doc)
    return {"success": True, "message": "Thank you for your feedback!"}


# DELETE a feedback entry (principal can remove spam/inappropriate entries)
@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: str):
    result = await feedback_col.delete_one({"id": feedback_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Feedback entry not found")
    return {"success": True}