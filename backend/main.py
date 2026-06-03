from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import auth, teachers, students, quizzes, announcements, settings

load_dotenv()

app = FastAPI(title="Prathibha LMS API")

# CORS — allow your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router,          prefix="/api/auth",          tags=["Auth"])
app.include_router(teachers.router,      prefix="/api/teachers",      tags=["Teachers"])
app.include_router(students.router,      prefix="/api/students",      tags=["Students"])
app.include_router(quizzes.router,       prefix="/api/quizzes",       tags=["Quizzes"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["Announcements"])
app.include_router(settings.router,      prefix="/api/settings",      tags=["Settings"])

@app.get("/")
def health():
    return {"status": "Prathibha LMS API is running"}