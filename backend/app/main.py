from collections import Counter
from io import BytesIO
import re

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from .rag import answer_question, retrieve_briefing
from .corpus import DOCUMENTS
from .ingestion import arxiv_documents, github_documents
from .store import get_documents, get_profile, initialize, upsert_documents, upsert_profile

app = FastAPI(title="SignalStack Profile API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    initialize()
    if not get_documents():
        upsert_documents(DOCUMENTS)

SKILLS = {
    "Python", "JavaScript", "TypeScript", "React", "Next.js", "FastAPI",
    "PostgreSQL", "Docker", "AWS", "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "LangChain", "LangGraph", "RAG", "LLM",
    "OpenAI", "Git", "GitHub", "Redis", "Kubernetes", "Node.js",
    "MongoDB", "SQL", "Java", "C++", "C", "HTML", "CSS",
}

PROJECT_HEADINGS = ("project", "experience", "internship", "work experience")


def extract_pdf_text(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()


def analyze_resume(text: str) -> dict:
    lowered = text.lower()
    skills = sorted(skill for skill in SKILLS if skill.lower() in lowered)
    lines = [line.strip(" •-\t") for line in text.splitlines() if line.strip()]
    projects = []
    is_project_area = False
    for line in lines:
        line_lower = line.lower()
        if any(heading in line_lower for heading in PROJECT_HEADINGS) and len(line) < 60:
            is_project_area = True
            continue
        if is_project_area and len(line) > 12 and len(projects) < 6:
            if not re.fullmatch(r"[A-Z &/]+", line):
                projects.append(line[:180])
    words = re.findall(r"[A-Za-z][A-Za-z+#.]{2,}", lowered)
    frequent_topics = [word for word, count in Counter(words).most_common(30) if count > 1 and word not in {"and", "the", "with", "for", "from", "using", "project"}]
    return {
        "skills": skills,
        "projects": projects[:4],
        "suggested_topics": frequent_topics[:10],
        "text_length": len(text),
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/briefing")
def briefing(payload: dict) -> dict:
    if not isinstance(payload.get("topics", []), list):
        raise HTTPException(status_code=422, detail="topics must be a list.")
    return retrieve_briefing(payload, documents=get_documents())


@app.post("/rag/ask")
def rag_ask(payload: dict) -> dict:
    question = str(payload.get("question", "")).strip()
    if not question:
        raise HTTPException(status_code=422, detail="A question is required.")
    profile = payload.get("profile", {})
    if not isinstance(profile, dict):
        raise HTTPException(status_code=422, detail="profile must be an object.")
    return answer_question(profile, question, documents=get_documents())


@app.put("/profiles/{profile_id}")
def save_profile(profile_id: str, payload: dict) -> dict:
    return upsert_profile(profile_id, payload)


@app.get("/profiles/{profile_id}")
def read_profile(profile_id: str) -> dict:
    profile = get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile


@app.post("/ingest/refresh")
def refresh_sources(payload: dict) -> dict:
    topics = [str(topic).strip() for topic in payload.get("topics", []) if str(topic).strip()][:3]
    if not topics:
        raise HTTPException(status_code=422, detail="Provide at least one topic.")
    documents = []
    errors = []
    for topic in topics:
        for name, loader in (("GitHub", github_documents), ("arXiv", arxiv_documents)):
            try:
                documents.extend(loader(topic))
            except Exception:
                errors.append(f"{name} could not be refreshed for {topic}.")
    return {"ingested": upsert_documents(documents) if documents else 0, "errors": errors}


@app.post("/profile/resume")
async def profile_resume(file: UploadFile = File(...)) -> dict:
    if file.content_type not in {"application/pdf", "text/plain"}:
        raise HTTPException(status_code=415, detail="Upload a PDF or plain-text resume.")
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume must be 5 MB or smaller.")
    try:
        text = data.decode("utf-8", errors="ignore") if file.content_type == "text/plain" else extract_pdf_text(data)
    except Exception as error:
        raise HTTPException(status_code=422, detail="The resume could not be read.") from error
    if not text:
        raise HTTPException(status_code=422, detail="No readable text was found in this resume.")
    return {"filename": file.filename, "analysis": analyze_resume(text)}
