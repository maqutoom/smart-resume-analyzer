import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path(__file__).parent / "data" / "jobs.json"
TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z+#.\-]*")


def load_jobs() -> list[dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    return text.lower().replace("-", " ").replace("_", " ")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(text_a: str, text_b: str) -> float:
    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)

    if not tokens_a or not tokens_b:
        return 0.0

    vector_a = Counter(tokens_a)
    vector_b = Counter(tokens_b)
    shared_terms = set(vector_a) & set(vector_b)

    dot_product = sum(vector_a[term] * vector_b[term] for term in shared_terms)
    magnitude_a = math.sqrt(sum(value * value for value in vector_a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def skill_in_text(skill: str, resume_text: str) -> bool:
    normalized_skill = normalize_text(skill)
    normalized_resume = normalize_text(resume_text)

    if normalized_skill in normalized_resume:
        return True

    skill_words = normalized_skill.split()
    return all(word in normalized_resume for word in skill_words)


def parse_manual_skills(skills_text: str) -> list[str]:
    skills = re.split(r"[\n,;]+", skills_text)
    cleaned_skills = []
    seen = set()

    for skill in skills:
        cleaned_skill = " ".join(skill.strip().split())
        skill_key = cleaned_skill.lower()

        if cleaned_skill and skill_key not in seen:
            cleaned_skills.append(cleaned_skill)
            seen.add(skill_key)

    return cleaned_skills


def match_resume_to_custom_job(
    resume_text: str,
    job_position: str,
    skills_text: str,
) -> dict[str, Any]:
    required_skills = parse_manual_skills(skills_text)

    if not required_skills:
        raise ValueError("Please enter at least one required skill.")

    matched_skills = [skill for skill in required_skills if skill_in_text(skill, resume_text)]
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]
    skill_score = len(matched_skills) / len(required_skills)
    job_text = f"{job_position} {' '.join(required_skills)}"
    text_score = cosine_similarity(resume_text, job_text)
    keyword_score = calculate_keyword_overlap(resume_text, job_text)
    final_score = (skill_score * 0.80) + (text_score * 0.15) + (keyword_score * 0.05)

    return {
        "id": "custom-job",
        "title": job_position.strip() or "Custom Job Position",
        "match_percentage": round(max(0, min(final_score * 100, 100)), 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_skills": required_skills,
        "skill_score": round(skill_score * 100, 2),
        "text_similarity": round(text_score * 100, 2),
        "keyword_overlap": round(keyword_score * 100, 2),
    }


def calculate_keyword_overlap(resume_text: str, job_description: str) -> float:
    resume_tokens = set(tokenize(resume_text))
    job_tokens = set(tokenize(job_description))

    if not job_tokens:
        return 0.0

    return len(resume_tokens & job_tokens) / len(job_tokens)


def match_resume_to_jobs(resume_text: str) -> list[dict[str, Any]]:
    jobs = load_jobs()
    results = []

    for job in jobs:
        skills = job["skills"]
        matched_skills = [skill for skill in skills if skill_in_text(skill, resume_text)]
        missing_skills = [skill for skill in skills if skill not in matched_skills]

        skill_score = len(matched_skills) / len(skills) if skills else 0.0
        text_score = cosine_similarity(resume_text, job["description"])
        keyword_score = calculate_keyword_overlap(resume_text, job["description"])

        final_score = (skill_score * 0.65) + (text_score * 0.25) + (keyword_score * 0.10)
        match_percentage = round(max(0, min(final_score * 100, 100)), 2)

        results.append(
            {
                "id": job["id"],
                "title": job["title"],
                "match_percentage": match_percentage,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "skill_score": round(skill_score * 100, 2),
                "text_similarity": round(text_score * 100, 2),
                "keyword_overlap": round(keyword_score * 100, 2),
            }
        )

    return sorted(results, key=lambda result: result["match_percentage"], reverse=True)
