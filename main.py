from fastapi import (
    FastAPI,
    Form,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from pypdf import PdfReader

from database import (
    create_database,
    add_user,
    get_user,
    get_jobs
)

from agent import scan_and_rank_jobs


app = FastAPI(
    title="JobPilot API",
    description="Autonomous Job Search & Application Agent",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


os.makedirs(
    "uploads",
    exist_ok=True
)


create_database()


@app.get("/")
def home():

    return {
        "project":
        "JobPilot - Autonomous Job Search & Application Agent",

        "status":
        "Backend Running 🚀"
    }


@app.post("/register")
async def register(

    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),

    qualification: str = Form(""),
    specialization: str = Form(""),
    college: str = Form(""),

    skills: str = Form(""),
    experience: str = Form(""),

    projects: str = Form(""),
    activities: str = Form(""),

    preferred_role: str = Form(""),
    preferred_location: str = Form(""),

    expected_salary: int = Form(0),

    work_preference: str = Form(""),

    about: str = Form(""),

    resume: UploadFile = File(...)
):

    # -------------------------
    # Save Resume
    # -------------------------

    file_path = os.path.join(
        "uploads",
        resume.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )


    # -------------------------
    # Extract Resume Text
    # -------------------------

    resume_text = ""

    if resume.filename.lower().endswith(
        ".pdf"
    ):

        reader = PdfReader(
            file_path
        )

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text


    # -------------------------
    # Create User
    # -------------------------

    data = {

        "full_name": full_name,
        "email": email,
        "phone": phone,

        "qualification":
            qualification,

        "specialization":
            specialization,

        "college":
            college,

        "skills":
            skills,

        "experience":
            experience,

        "projects":
            projects,

        "activities":
            activities,

        "preferred_role":
            preferred_role,

        "preferred_location":
            preferred_location,

        "expected_salary":
            expected_salary,

        "work_preference":
            work_preference,

        "resume_filename":
            resume.filename,

        "resume_text":
            resume_text,

        "about":
            about
    }


    user_id = add_user(data)


    return {

        "success": True,

        "message":
            "Profile created successfully",

        "user_id":
            user_id,

        "resume_text_extracted":
            len(resume_text) > 0
    }


@app.get("/jobs/{user_id}")
def recommended_jobs(
    user_id: int
):

    results = scan_and_rank_jobs(
        user_id
    )

    return {

        "user_id":
            user_id,

        "total_jobs":
            len(results),

        "recommendations":
            results
    }