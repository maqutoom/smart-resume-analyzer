const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeResume({ file, text }) {
  const formData = new FormData();

  if (file) {
    formData.append("resume_file", file);
  } else {
    formData.append("resume_text", text);
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Resume analysis failed.");
  }

  return response.json();
}

