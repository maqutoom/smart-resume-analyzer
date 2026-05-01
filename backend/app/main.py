from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .matcher import match_resume_to_jobs
from .resume_parser import extract_text_from_upload
from .suggestions import build_suggestions, score_label


app = FastAPI(title="Smart Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Smart Resume Analyzer API is running"}


@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile | None = File(default=None),
    resume_text: str | None = Form(default=None),
) -> dict:
    extracted_text = ""

    if resume_file:
        file_bytes = await resume_file.read()
        extracted_text = extract_text_from_upload(
            resume_file.filename or "",
            resume_file.content_type,
            file_bytes,
        )
    elif resume_text:
        extracted_text = resume_text.strip()

    if not extracted_text:
        raise HTTPException(status_code=400, detail="Please upload a resume or paste resume text.")

    matches = match_resume_to_jobs(extracted_text)
    best_match = matches[0]

    return {
        "best_role": best_match["title"],
        "match_percentage": best_match["match_percentage"],
        "match_label": score_label(best_match["match_percentage"]),
        "matched_skills": best_match["matched_skills"],
        "missing_skills": best_match["missing_skills"],
        "suggestions": build_suggestions(best_match, extracted_text),
        "all_matches": matches,
        "resume_word_count": len(extracted_text.split()),
    }

