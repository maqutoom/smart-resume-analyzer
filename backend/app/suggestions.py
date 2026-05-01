from typing import Any


def score_label(score: float) -> str:
    if score >= 80:
        return "Excellent match"
    if score >= 60:
        return "Good match"
    if score >= 40:
        return "Partial match"
    return "Low match"


def build_suggestions(best_match: dict[str, Any], resume_text: str) -> list[str]:
    suggestions = []
    missing_skills = best_match["missing_skills"][:5]

    if missing_skills:
        suggestions.append(
            "Add projects, coursework, or certifications that show these skills: "
            + ", ".join(missing_skills)
            + "."
        )

    if len(resume_text.split()) < 180:
        suggestions.append("Add more detail to your resume, especially project impact, tools used, and measurable results.")

    if not any(char.isdigit() for char in resume_text):
        suggestions.append("Include numbers where possible, such as percentages, users, time saved, or performance improvements.")

    if "project" not in resume_text.lower() and "projects" not in resume_text.lower():
        suggestions.append("Add a projects section that clearly connects your work to the role you want.")

    if not suggestions:
        suggestions.append("Your resume is aligned well. Improve it further by adding stronger action verbs and measurable achievements.")

    return suggestions

