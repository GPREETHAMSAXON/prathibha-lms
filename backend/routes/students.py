from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import random
import string
from database import students_col

router = APIRouter()


# --- PYDANTIC MODELS ---

class QuizScore(BaseModel):
    quizId: str
    quizTitle: str
    score: int
    totalQuestions: int
    date: str


class Student(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str
    classNum: str
    quizScores: List[QuizScore] = []


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    classNum: Optional[str] = None


# --- HELPER ---

def generate_id():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
    return f"st_{suffix}"


# --- ROUTES ---

# GET all students (principal only — password excluded)
@router.get("/")
async def get_all_students():
    students = await students_col.find({}, {"_id": 0, "password": 0}).to_list(None)
    return students


# GET single student by ID
@router.get("/{student_id}")
async def get_student(student_id: str):
    student = await students_col.find_one(
        {"id": student_id},
        {"_id": 0, "password": 0}
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# GET students filtered by class
@router.get("/class/{class_num}")
async def get_students_by_class(class_num: str):
    students = await students_col.find(
        {"classNum": class_num},
        {"_id": 0, "password": 0}
    ).to_list(None)
    return students


# POST create a new student
@router.post("/")
async def create_student(student: Student):
    # Check for duplicate email
    existing = await students_col.find_one({"email": student.email.lower().strip()})
    if existing:
        raise HTTPException(status_code=400, detail="A student with this email already exists")

    doc = student.dict()
    doc["email"] = doc["email"].lower().strip()
    if not doc["id"]:
        doc["id"] = generate_id()
    if doc["quizScores"] is None:
        doc["quizScores"] = []

    await students_col.insert_one(doc)
    doc.pop("password", None)   # never return password
    return {"success": True, "student": doc}


# PUT update student details
@router.put("/{student_id}")
async def update_student(student_id: str, updates: StudentUpdate):
    existing = await students_col.find_one({"id": student_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    await students_col.update_one({"id": student_id}, {"$set": update_data})
    return {"success": True}


# POST submit a quiz score for a student
@router.post("/{student_id}/quiz-score")
async def submit_quiz_score(student_id: str, score: QuizScore):
    student = await students_col.find_one({"id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Prevent duplicate score entries for the same quiz
    existing_scores = student.get("quizScores", [])
    already_attempted = any(s["quizId"] == score.quizId for s in existing_scores)
    if already_attempted:
        raise HTTPException(status_code=400, detail="Quiz already attempted by this student")

    await students_col.update_one(
        {"id": student_id},
        {"$push": {"quizScores": score.dict()}}
    )
    return {"success": True}


# GET quiz scores for a specific student
@router.get("/{student_id}/quiz-scores")
async def get_quiz_scores(student_id: str):
    student = await students_col.find_one({"id": student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.get("quizScores", [])


# DELETE a student
@router.delete("/{student_id}")
async def delete_student(student_id: str):
    result = await students_col.delete_one({"id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True}