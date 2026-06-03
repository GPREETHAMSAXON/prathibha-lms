from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
import string
from database import quizzes_col

router = APIRouter()


# --- PYDANTIC MODELS ---

class Question(BaseModel):
    question: str
    options: List[str]          # exactly 4 options
    correctAnswer: str


class Quiz(BaseModel):
    id: Optional[str] = None
    title: str
    subject: str
    classNum: str
    questions: List[Question]
    createdBy: str              # teacher id e.g. "t_suresh"
    isApproved: bool = False    # principal must approve before students see it


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    classNum: Optional[str] = None
    questions: Optional[List[Question]] = None
    isApproved: Optional[bool] = None


# --- HELPER ---

def generate_id():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"q_{suffix}"


# --- ROUTES ---

# GET all quizzes (principal/teacher view — all quizzes)
@router.get("/")
async def get_all_quizzes():
    quizzes = await quizzes_col.find({}, {"_id": 0}).to_list(None)
    return quizzes


# GET only approved quizzes (student-facing)
@router.get("/approved")
async def get_approved_quizzes():
    quizzes = await quizzes_col.find(
        {"isApproved": True},
        {"_id": 0}
    ).to_list(None)
    return quizzes


# GET quizzes filtered by class (approved only — for students)
@router.get("/class/{class_num}")
async def get_quizzes_by_class(class_num: str):
    quizzes = await quizzes_col.find(
        {"classNum": class_num, "isApproved": True},
        {"_id": 0}
    ).to_list(None)
    return quizzes


# GET quizzes created by a specific teacher
@router.get("/teacher/{teacher_id}")
async def get_quizzes_by_teacher(teacher_id: str):
    quizzes = await quizzes_col.find(
        {"createdBy": teacher_id},
        {"_id": 0}
    ).to_list(None)
    return quizzes


# GET single quiz by ID
@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str):
    quiz = await quizzes_col.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


# POST create a new quiz (teacher)
@router.post("/")
async def create_quiz(quiz: Quiz):
    if len(quiz.questions) == 0:
        raise HTTPException(status_code=400, detail="A quiz must have at least one question")

    # Validate each question has exactly 4 options
    for i, q in enumerate(quiz.questions):
        if len(q.options) != 4:
            raise HTTPException(
                status_code=400,
                detail=f"Question {i + 1} must have exactly 4 options"
            )
        if q.correctAnswer not in q.options:
            raise HTTPException(
                status_code=400,
                detail=f"Question {i + 1}: correctAnswer must be one of the provided options"
            )

    doc = quiz.dict()
    if not doc["id"]:
        doc["id"] = generate_id()

    await quizzes_col.insert_one(doc)
    return {"success": True, "quizId": doc["id"]}


# PUT update a quiz (teacher can edit own quiz; principal can approve)
@router.put("/{quiz_id}")
async def update_quiz(quiz_id: str, updates: QuizUpdate):
    existing = await quizzes_col.find_one({"id": quiz_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Quiz not found")

    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # Validate questions if being updated
    if "questions" in update_data:
        for i, q in enumerate(update_data["questions"]):
            if len(q["options"]) != 4:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {i + 1} must have exactly 4 options"
                )

    await quizzes_col.update_one({"id": quiz_id}, {"$set": update_data})
    return {"success": True}


# PATCH approve a quiz (principal only)
@router.patch("/{quiz_id}/approve")
async def approve_quiz(quiz_id: str):
    existing = await quizzes_col.find_one({"id": quiz_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Quiz not found")

    await quizzes_col.update_one({"id": quiz_id}, {"$set": {"isApproved": True}})
    return {"success": True, "message": "Quiz approved and now visible to students"}


# PATCH unapprove / withdraw a quiz (principal only)
@router.patch("/{quiz_id}/unapprove")
async def unapprove_quiz(quiz_id: str):
    existing = await quizzes_col.find_one({"id": quiz_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Quiz not found")

    await quizzes_col.update_one({"id": quiz_id}, {"$set": {"isApproved": False}})
    return {"success": True, "message": "Quiz withdrawn from students"}


# DELETE a quiz
@router.delete("/{quiz_id}")
async def delete_quiz(quiz_id: str):
    result = await quizzes_col.delete_one({"id": quiz_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"success": True}