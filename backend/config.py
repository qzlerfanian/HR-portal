import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR", ROOT / "data")).resolve()
RESUMES_DIR = DATA_DIR / "resumes"
DB_PATH = DATA_DIR / "talentflow.sqlite3"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini").strip()
HR_ADMIN_PASSWORD = os.getenv("HR_ADMIN_PASSWORD", "")
_session_secret = os.getenv("SESSION_SECRET", "").strip()
_session_secret_file = DATA_DIR / ".session_secret"
if not _session_secret:
    if not _session_secret_file.exists():
        _session_secret_file.write_text(secrets.token_urlsafe(48), encoding="utf-8")
    _session_secret = _session_secret_file.read_text(encoding="utf-8").strip()
SESSION_SECRET = _session_secret
SESSION_COOKIE = "talentflow_hr_session"
MAX_RESUME_BYTES = 10 * 1024 * 1024
MAX_BRIEF_BYTES = 15 * 1024 * 1024

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "image/jpeg",
    "image/png",
    "image/webp",
}

DATA_DIR.mkdir(parents=True, exist_ok=True)
RESUMES_DIR.mkdir(parents=True, exist_ok=True)
