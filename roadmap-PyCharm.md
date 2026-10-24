# Run TalentFlow in PyCharm on Windows

## Open the project

In PyCharm, select **File → Open** and choose the `talentflow-app` folder containing `requirements.txt` and `run_local.py`.

The backend uses Python/FastAPI. The web interface uses React and requires Node.js 22.13 or newer.

## Install dependencies once

Open the PyCharm terminal at the project root and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm ci
```

If `py -3` is unavailable, use Python 3.10+ and run `python -m venv .venv`. In PyCharm, choose `.venv\Scripts\python.exe` under **Settings → Project → Python Interpreter**.

## Configure AI and HR login

Create or edit `.env` in the project root:

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
HR_ADMIN_PASSWORD=choose-a-strong-password
```

Add your OpenAI API key to `OPENAI_API_KEY`. `SESSION_SECRET` is generated locally in `data/.session_secret` if left blank. Do not put API keys in the website or commit `.env`.

## Start the app

Right-click `run_local.py` in PyCharm and choose **Run 'run_local'**. This starts FastAPI on port 8000 and the website on port 5173. Open:

`http://localhost:5173`

The public careers page is `/`; the HR portal is `/admin`. Sign in with `HR_ADMIN_PASSWORD`. Press `Ctrl+C` in the run window to stop both services.

If PyCharm does not create a run configuration, run `python run_local.py` in the project terminal.

SQLite and resumes are stored in `data/`. Resume files can only be downloaded from the authenticated HR portal.
