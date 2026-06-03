from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["prathibha_lms"]

# Collections
teachers_col     = db["teachers"]
students_col     = db["students"]
quizzes_col      = db["quizzes"]
announcements_col = db["announcements"]
feedback_col     = db["feedback"]
settings_col     = db["settings"]