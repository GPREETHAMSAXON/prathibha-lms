from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from database import teachers_col

router = APIRouter()

@router.get("/")
async def get_teachers():
    teachers = await teachers_col.find({}, {"_id": 0}).to_list(None)
    return teachers

@router.post("/")
async def add_teacher(teacher: dict):
    await teachers_col.insert_one(teacher)
    return {"success": True}

@router.put("/{teacher_id}")
async def update_teacher(teacher_id: str, updates: dict):
    await teachers_col.update_one({"id": teacher_id}, {"$set": updates})
    return {"success": True}

@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: str):
    await teachers_col.delete_one({"id": teacher_id})
    return {"success": True}