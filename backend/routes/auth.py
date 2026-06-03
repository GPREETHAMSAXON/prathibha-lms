from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import teachers_col, students_col

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(body: LoginRequest):
    email = body.email.lower().strip()
    password = body.password

    # Principal check
    if email == "principal@prathibha.com" and password == "admin123":
        return {"success": True, "user": {
            "id": "principal", "name": "Dr. K. S. Rao (Principal)",
            "email": email, "role": "principal"
        }}

    # Teacher check
    teacher = await teachers_col.find_one({"email": email, "password": password})
    if teacher:
        if teacher.get("status") != "Active":
            raise HTTPException(400, "Account deactivated")
        return {"success": True, "user": {
            "id": teacher["id"], "name": teacher["name"],
            "email": teacher["email"], "role": "teacher",
            "assignedClasses": teacher["assignedClasses"],
            "assignedSubjects": teacher["assignedSubjects"]
        }}

    # Student check
    student = await students_col.find_one({"email": email, "password": password})
    if student:
        return {"success": True, "user": {
            "id": student["id"], "name": student["name"],
            "email": student["email"], "role": "student",
            "classNum": student["classNum"]
        }}

    raise HTTPException(401, "Invalid email or password")