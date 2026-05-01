import { useMemo, useState } from "react";
import { analyzeResume } from "./api";

const sampleResume = `Frontend Developer with experience building responsive React applications.
Skills include React, JavaScript, HTML, CSS, Git, REST API integration, responsive design, and UI debugging.
Built projects using reusable components, form validation, and dashboard layouts.`;

function getScoreClass(score) {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "partial";
  return "low";
}

function App() {
  const [resumeText, setResumeText] = useState(sampleResume);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const scoreClass = useMemo(() => {
    if (!result) return "";
    return getScoreClass(result.match_percentage);
  }, [result]);

  async function handleAnalyze(event) {
    event.preventDefault();
    setError("");
    setResult(null);
    setIsLoading(true);

    try {
      const analysis = await analyzeResume({ file, text: resumeText });
      setResult(analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <div className="intro">
          <div>
            <p className="eyebrow">AI Resume Project</p>
            <h1>Smart Resume Analyzer & Job Matcher</h1>
            <p>
              Upload or paste a resume to compare it with real job-role profiles and get a clear percentage match.
            </p>
          </div>
          <div className="metric-strip" aria-label="Project features">
            <span>Role match</span>
            <span>Skill gaps</span>
            <span>Resume tips</span>
          </div>
        </div>

        <div className="content-grid">
          <form className="panel analyzer" onSubmit={handleAnalyze}>
            <div className="panel-heading">
              <span className="icon-mark" aria-hidden="true">CV</span>
              <div>
                <h2>Resume Input</h2>
                <p>Use PDF, TXT, or pasted text.</p>
              </div>
            </div>

            <label className="upload-box">
              <span className="small-icon" aria-hidden="true">Upload</span>
              <span>{file ? file.name : "Choose resume file"}</span>
              <input
                type="file"
                accept=".pdf,.txt,text/plain,application/pdf"
                onChange={(event) => setFile(event.target.files?.[0] || null)}
              />
            </label>

            <label className="textarea-label" htmlFor="resumeText">
              Paste resume text
            </label>
            <textarea
              id="resumeText"
              value={resumeText}
              onChange={(event) => setResumeText(event.target.value)}
              placeholder="Paste your resume text here..."
            />

            {error && <p className="error">{error}</p>}

            <button className="primary-button" type="submit" disabled={isLoading}>
              <span className={isLoading ? "button-dot spin" : "button-dot"} aria-hidden="true" />
              {isLoading ? "Analyzing..." : "Analyze Resume"}
            </button>
          </form>

          <section className="panel results" aria-live="polite">
            {!result ? (
              <div className="empty-state">
                <span className="empty-icon" aria-hidden="true">%</span>
                <h2>Your match report will appear here</h2>
                <p>Try the sample resume, then replace it with your own details.</p>
              </div>
            ) : (
              <>
                <div className="score-header">
                  <div>
                    <p className="eyebrow">Best Fit</p>
                    <h2>{result.best_role}</h2>
                    <p>{result.match_label}</p>
                  </div>
                  <div className={`score-badge ${scoreClass}`}>
                    <strong>{result.match_percentage}%</strong>
                    <span>Match</span>
                  </div>
                </div>

                <div className="section-block">
                  <h3>All Role Matches</h3>
                  <div className="match-list">
                    {result.all_matches.map((match) => (
                      <div className="match-row" key={match.id}>
                        <div>
                          <strong>{match.title}</strong>
                          <span>{match.matched_skills.length} skills matched</span>
                        </div>
                        <div className="bar-track" aria-label={`${match.title} ${match.match_percentage}% match`}>
                          <div className="bar-fill" style={{ width: `${match.match_percentage}%` }} />
                        </div>
                        <b>{match.match_percentage}%</b>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="two-column">
                  <div className="section-block">
                    <h3>Matched Skills</h3>
                    <div className="skill-cloud">
                      {result.matched_skills.length ? result.matched_skills.map((skill) => <span key={skill}>{skill}</span>) : <em>No direct skill matches found.</em>}
                    </div>
                  </div>

                  <div className="section-block">
                    <h3>Missing Skills</h3>
                    <div className="skill-cloud missing">
                      {result.missing_skills.slice(0, 8).map((skill) => <span key={skill}>{skill}</span>)}
                    </div>
                  </div>
                </div>

                <div className="section-block">
                  <h3>Resume Improvements</h3>
                  <ul className="suggestions">
                    {result.suggestions.map((suggestion) => (
                      <li key={suggestion}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              </>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;
