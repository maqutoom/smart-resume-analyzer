# Smart Resume Analyzer & Job Matcher

A beginner-friendly AI/NLP web app that analyzes a resume, compares it with job roles, and returns match percentages, matched skills, missing skills, and resume improvement suggestions.

## Project Structure

```text
smart-resume-analyzer/
  backend/
    app/
      data/jobs.json
      main.py
      matcher.py
      resume_parser.py
      suggestions.py
    requirements.txt
  frontend/
    index.html
    package.json
    src/
      App.jsx
      api.js
      main.jsx
      styles.css
```

## Step 1: Start the Backend

```powershell
cd "D:\Python Project\backend"
python -m venv .venv
python -m pip install --target .venv\Lib\site-packages -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Or use the included Windows helper:

```powershell
cd "D:\Python Project\backend"
.\run-backend.bat
```

Backend URL:

```text
http://127.0.0.1:8000
```

## Step 2: Start the Frontend

Open another terminal:

```powershell
cd "D:\Python Project\frontend"
npm.cmd install
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

Or use the included Windows helper:

```powershell
cd "D:\Python Project\frontend"
.\run-frontend.bat
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Step 3: Use the App

1. Paste resume text or upload a `.txt` or `.pdf` resume.
2. Click **Analyze Resume**.
3. Review:
   - Best-fit job role
   - Match percentage
   - Matched skills
   - Missing skills
   - Resume improvement suggestions

## How Match Percentage Works

The backend compares resume text with each job role using:

- Skill overlap
- Keyword overlap
- Text similarity

The final match percentage is a weighted score from `0` to `100`.
