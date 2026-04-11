import re

SUBJECT_KEYWORDS = {
    "machine learning": "Machine Learning",
    "data science": "Data Science",
    "python": "Python",
    "programming": "Programming",
}


def parse_contract_description(text: str):
    lowered = text.lower()
    subject = "Programming"

    for key, normalized in SUBJECT_KEYWORDS.items():
        if key in lowered:
            subject = normalized
            break

    required_trainers = 2
    match = re.search(r"(\d+)\s+(?:trainers|trainer)", lowered)
    if match:
        required_trainers = int(match.group(1))

    return {"subject": subject, "required_trainers": required_trainers}


def analyze_cv(filename: str, subject: str, skills: str, years_experience: int):
    score = 0
    if subject.lower() in (skills or "").lower() or subject.lower() in filename.lower():
        score += 50

    if years_experience > 3:
        score += 30
    else:
        score += 10

    return min(score, 100)
