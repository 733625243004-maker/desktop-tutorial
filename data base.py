import sqlite3

DATABASE = "jobs.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        qualification TEXT,
        specialization TEXT,
        college TEXT,
        skills TEXT,
        experience TEXT,
        projects TEXT,
        activities TEXT,
        preferred_role TEXT,
        preferred_location TEXT,
        expected_salary INTEGER,
        work_preference TEXT,
        resume_filename TEXT,
        resume_text TEXT,
        about TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        job_title TEXT,
        required_skills TEXT,
        qualification TEXT,
        experience_required TEXT,
        location TEXT,
        salary_min INTEGER,
        salary_max INTEGER,
        description TEXT,
        application_url TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_id INTEGER,
        fit_score REAL,
        matching_skills TEXT,
        missing_skills TEXT,
        reason TEXT,
        rank INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_id INTEGER,
        status TEXT,
        approval_status TEXT,
        submitted_at TEXT,
        follow_up_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        result TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_user(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (
        full_name, email, phone, qualification,
        specialization, college, skills,
        experience, projects, activities,
        preferred_role, preferred_location,
        expected_salary, work_preference,
        resume_filename, resume_text, about
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["full_name"],
        data["email"],
        data["phone"],
        data["qualification"],
        data["specialization"],
        data["college"],
        data["skills"],
        data["experience"],
        data["projects"],
        data["activities"],
        data["preferred_role"],
        data["preferred_location"],
        data["expected_salary"],
        data["work_preference"],
        data["resume_filename"],
        data["resume_text"],
        data["about"]
    ))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_jobs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def add_job(job):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jobs (
        company_name,
        job_title,
        required_skills,
        qualification,
        experience_required,
        location,
        salary_min,
        salary_max,
        description,
        application_url
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, job)

    conn.commit()
    conn.close()