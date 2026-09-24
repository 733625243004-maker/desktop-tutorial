def clean_list(text):

    if not text:
        return []

    return [
        item.strip().lower()
        for item in text.split(",")
        if item.strip()
    ]


def calculate_match(user, job):

    user_skills = set(
        clean_list(user[7])
    )

    required_skills = set(
        clean_list(job[3])
    )

    matching_skills = user_skills.intersection(
        required_skills
    )

    missing_skills = required_skills.difference(
        user_skills
    )

    # -------------------------
    # 1. Skills Score - 40%
    # -------------------------

    if required_skills:

        skill_score = (
            len(matching_skills)
            / len(required_skills)
        ) * 40

    else:

        skill_score = 0


    # -------------------------
    # 2. Qualification - 20%
    # -------------------------

    user_qualification = (
        user[4] or ""
    ).lower()

    job_qualification = (
        job[4] or ""
    ).lower()

    qualification_score = 0

    if (
        user_qualification
        and user_qualification in job_qualification
    ):
        qualification_score = 20


    # -------------------------
    # 3. Experience - 15%
    # -------------------------

    user_experience = (
        user[8] or ""
    ).lower()

    job_experience = (
        job[5] or ""
    ).lower()

    experience_score = 0

    if "fresher" in job_experience:

        if "fresher" in user_experience:
            experience_score = 15

    elif user_experience:
        experience_score = 10


    # -------------------------
    # 4. Location - 10%
    # -------------------------

    user_location = (
        user[12] or ""
    ).lower()

    job_location = (
        job[6] or ""
    ).lower()

    location_score = 0

    if (
        user_location
        and job_location
        and (
            user_location in job_location
            or job_location in user_location
        )
    ):
        location_score = 10


    # -------------------------
    # 5. Role - 15%
    # -------------------------

    preferred_role = (
        user[11] or ""
    ).lower()

    job_title = (
        job[2] or ""
    ).lower()

    role_score = 0

    if (
        preferred_role
        and (
            preferred_role in job_title
            or job_title in preferred_role
        )
    ):
        role_score = 15


    total_score = (
        skill_score
        + qualification_score
        + experience_score
        + location_score
        + role_score
    )


    reason = []

    if matching_skills:
        reason.append(
            "Matching skills: "
            + ", ".join(matching_skills)
        )

    if qualification_score:
        reason.append(
            "Qualification matches"
        )

    if experience_score:
        reason.append(
            "Experience requirement matches"
        )

    if location_score:
        reason.append(
            "Preferred location matches"
        )

    if role_score:
        reason.append(
            "Preferred job role matches"
        )


    return {
        "score": round(total_score, 2),
        "matching_skills": list(matching_skills),
        "missing_skills": list(missing_skills),
        "reason": " | ".join(reason)
    }