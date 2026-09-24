from database import get_user, get_jobs
from matcher import calculate_match


def scan_and_rank_jobs(user_id):

    user = get_user(user_id)

    jobs = get_jobs()

    results = []


    for job in jobs:

        match = calculate_match(
            user,
            job
        )

        results.append({

            "job_id": job[0],

            "company": job[1],

            "title": job[2],

            "location": job[6],

            "salary": f"₹{job[7]} - ₹{job[8]}",

            "score": match["score"],

            "matching_skills":
                match["matching_skills"],

            "missing_skills":
                match["missing_skills"],

            "reason":
                match["reason"],

            "application_url":
                job[10]
        })


    # Highest score first

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # Add ranking

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index


    return results