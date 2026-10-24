# Configure the OpenAI API

Set your OpenAI API key in `.env` at the project root. The key is read only by the Python backend and is never sent to the browser.

```dotenv
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5.4-mini
HR_ADMIN_PASSWORD=choose-a-strong-password
```

After editing `.env`, restart the app with `python run_local.py`. The local `.env` and `data/` folder are excluded from Git. Never put API keys in the website, frontend code, Git, or chat.
