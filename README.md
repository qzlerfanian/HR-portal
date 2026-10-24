# TalentFlow | AI Recruitment Platform

TalentFlow is a recruiting web app with a React interface and a **Python/FastAPI** backend. HR can create job posts from PDF, Word, or image briefs, publish and edit jobs, receive resumes, and review AI-assisted job-fit analysis. Data is stored locally in SQLite and a private folder.

## Run locally in PyCharm

See [PyCharm Setup](./roadmap-PyCharm) for Windows setup. In short:

1. Install Node.js 22.13+ and Python 3.10+.
2. Create a Python environment and install dependencies:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   npm ci
   ```

3. Set `OPENAI_API_KEY` and `HR_ADMIN_PASSWORD` in `.env`.
4. Run `run_local.py` in PyCharm and open `http://localhost:5173`.

`run_local.py` starts FastAPI at port 8000 and the web app at port 5173. Vite proxies `/backend` requests to Python. FastAPI Swagger is available at `http://localhost:8000/docs`.

## Data and privacy

- SQLite and uploaded resumes are stored under `data/`, which is excluded from Git.
- AI API keys are read by the Python backend only. The local `.env` file is excluded from Git.
- Recruitment briefs and resumes are sent to the selected AI provider for job-post generation and resume analysis. Applicants are asked for consent.
- Resume downloads and HR APIs require an authenticated HR session.
- AI scores support human review and do not make hiring decisions. Protected characteristics are excluded from scoring instructions.

## Project structure

- `backend/`: FastAPI, admin authentication, SQLite, and OpenAI integration
- `app/`: public careers page and HR portal
- `requirements.txt`: Python dependencies
- `.env.example`: local configuration template; keep the real `.env` private
- `data/`: local database and private resume storage (created automatically)
