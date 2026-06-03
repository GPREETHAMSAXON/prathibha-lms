"""
Prathibha LMS - One-Time Database Seeder
Run this ONCE after deploying to push all default data into MongoDB Atlas.

Usage:
    python seed.py

Make sure your .env file has MONGO_URI set before running.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# --- DEFAULT DATA (mirrored from database.js) ---

DEFAULT_TEACHERS = [
    {
        "id": "t_suresh",
        "name": "Suresh Kumar",
        "email": "suresh.maths@prathibha.com",
        "password": "teacher123",
        "assignedClasses": ["8", "9", "10"],
        "assignedSubjects": ["Mathematics", "Computer Science"],
        "status": "Active"
    },
    {
        "id": "t_geetha",
        "name": "Geetha Rani",
        "email": "geetha.science@prathibha.com",
        "password": "teacher123",
        "assignedClasses": ["6", "7", "8"],
        "assignedSubjects": ["Science"],
        "status": "Active"
    },
    {
        "id": "t_ramesh",
        "name": "Ramesh Sharma",
        "email": "ramesh.english@prathibha.com",
        "password": "teacher123",
        "assignedClasses": ["1", "2", "3", "4", "5", "6"],
        "assignedSubjects": ["English", "Social Studies"],
        "status": "Active"
    }
]

DEFAULT_STUDENTS = [
    {
        "id": "st_anil",
        "name": "Anil Reddy",
        "email": "anil@student.com",
        "password": "student123",
        "classNum": "10",
        "quizScores": [
            {
                "quizId": "q_1",
                "quizTitle": "Trigonometric Identities Quiz",
                "score": 3,
                "totalQuestions": 3,
                "date": "2026-06-01"
            }
        ]
    }
]

DEFAULT_QUIZZES = [
    {
        "id": "q_1",
        "title": "Class 10 - Trigonometric Identities Quiz",
        "subject": "Mathematics",
        "classNum": "10",
        "questions": [
            {
                "question": "What is the value of sin²θ + cos²θ?",
                "options": ["0", "1", "-1", "2"],
                "correctAnswer": "1"
            },
            {
                "question": "If sin θ = 3/5, what is the value of cos θ?",
                "options": ["4/5", "3/4", "5/3", "2/5"],
                "correctAnswer": "4/5"
            },
            {
                "question": "What is 1 + tan²θ equal to?",
                "options": ["sin²θ", "cos²θ", "sec²θ", "cosec²θ"],
                "correctAnswer": "sec²θ"
            }
        ],
        "createdBy": "t_suresh",
        "isApproved": True
    },
    {
        "id": "q_2",
        "title": "Class 8 - Plant Cell & Animal Cell Anatomy Quiz",
        "subject": "Science",
        "classNum": "8",
        "questions": [
            {
                "question": "Which organelle is known as the powerhouse of the cell?",
                "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi Apparatus"],
                "correctAnswer": "Mitochondria"
            },
            {
                "question": "Which of the following is present ONLY in plant cells?",
                "options": ["Cell Membrane", "Cell Wall", "Cytoplasm", "Nucleus"],
                "correctAnswer": "Cell Wall"
            },
            {
                "question": "What green pigment is responsible for photosynthesis?",
                "options": ["Chlorophyll", "Hemoglobin", "Carotene", "Xanthophyll"],
                "correctAnswer": "Chlorophyll"
            }
        ],
        "createdBy": "t_geetha",
        "isApproved": True
    },
    {
        "id": "q_3",
        "title": "Class 6 - Perfect Tenses Comprehension",
        "subject": "English",
        "classNum": "6",
        "questions": [
            {
                "question": "Choose the correct Present Perfect form: 'She ______ her homework already.'",
                "options": ["finish", "finished", "has finished", "had finished"],
                "correctAnswer": "has finished"
            },
            {
                "question": "Identify the tense: 'By next week, we will have lived here for five years.'",
                "options": ["Future Perfect", "Present Perfect", "Past Perfect", "Simple Future"],
                "correctAnswer": "Future Perfect"
            }
        ],
        "createdBy": "t_ramesh",
        "isApproved": True
    }
]

DEFAULT_ANNOUNCEMENTS = [
    {
        "id": "a_1",
        "title": "Welcome to Prathibha High School Digital Learning Hub",
        "description": "In alignment with United Nations SDG 4 (Quality Education), our school is proud to introduce our centralized portal. Students can now access high-quality study notes, interactive video sessions, and assignments, while Teachers and the Principal manage all resources seamlessly. Let's learn today and lead tomorrow!",
        "createdBy": "Principal (Admin)",
        "date": "2026-06-01",
        "classNum": "All"
    },
    {
        "id": "a_2",
        "title": "First Term Examination Timetable Released",
        "description": "The term-end examinations for Classes 1 to 10 are scheduled to begin from June 15, 2026. Detailed schedules for each class have been uploaded. Please consult your respective subject teachers for revision worksheets and doubt clearing.",
        "createdBy": "Principal (Admin)",
        "date": "2026-06-01",
        "classNum": "All"
    },
    {
        "id": "a_3",
        "title": "Mathematics Revision Session for Class 10",
        "description": "A special online live doubt-clearing session for Class 10 Trigonometry will take place this Thursday at 4:00 PM. Please complete the quiz on trigonometric identities before joining the session.",
        "createdBy": "Suresh Kumar",
        "date": "2026-05-29",
        "classNum": "10"
    },
    {
        "id": "a_4",
        "title": "Science Lab Project: Cell Models Submission",
        "description": "All Class 8 students must upload photo submissions of their 3D animal/plant cell models in the study materials section by Saturday. Late entries will not be recorded in internal grades.",
        "createdBy": "Geetha Rani",
        "date": "2026-05-30",
        "classNum": "8"
    }
]

DEFAULT_FEEDBACK = [
    {
        "id": "f_1",
        "name": "Rajesh Varma",
        "classNum": "10",
        "email": "rajesh.parent@gmail.com",
        "message": "This portal is a fantastic initiative! It has helped my son revise for the Class 10 board exams extremely effectively. The quizzes give instant feedback, which is super helpful.",
        "date": "2026-06-01"
    }
]

DEFAULT_SETTINGS = {
    "schoolName": "Prathibha High School",
    "motto": "Learn Today, Lead Tomorrow",
    "address": "Plot 45-48, Education Enclave, Near Science Center, Hyderabad, TS, India",
    "phone": "+91 40 2345 6789",
    "email": "info@prathibhaschool.edu.in",
    "logoText": "PHS",
    "visitorCount": 1248
}


# --- SEEDER ---

async def seed():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ ERROR: MONGO_URI not found in .env file. Aborting.")
        return

    print("🔌 Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(mongo_uri)
    db = client["prathibha_lms"]

    # Test connection
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB Atlas successfully\n")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    collections = {
        "teachers":      (db["teachers"],      DEFAULT_TEACHERS),
        "students":      (db["students"],       DEFAULT_STUDENTS),
        "quizzes":       (db["quizzes"],        DEFAULT_QUIZZES),
        "announcements": (db["announcements"],  DEFAULT_ANNOUNCEMENTS),
        "feedback":      (db["feedback"],       DEFAULT_FEEDBACK),
    }

    for name, (col, data) in collections.items():
        count = await col.count_documents({})
        if count > 0:
            # Already has data — skip to avoid duplicates
            print(f"⏭️  {name}: already has {count} document(s) — skipping")
        else:
            await col.insert_many(data)
            print(f"✅ {name}: inserted {len(data)} document(s)")

    # Settings is a single document — upsert it
    settings_col = db["settings"]
    settings_count = await settings_col.count_documents({})
    if settings_count > 0:
        print(f"⏭️  settings: already exists — skipping")
    else:
        await settings_col.insert_one(DEFAULT_SETTINGS)
        print(f"✅ settings: inserted default school settings")

    print("\n🎉 Seeding complete! Your MongoDB Atlas database is ready.")
    print("👉 You can now start the FastAPI server: uvicorn main:app --reload")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())