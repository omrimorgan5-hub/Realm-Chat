# Chat-Project

Short description

A lightweight chat project with a Python backend and static web frontend. This repository contains authentication and messaging modules, simple web pages for login/signup/OTP, and utilities for testing.

Quick links

- Project root: `.`
- Server code: `src/chat_project/api` (auth and messages servers)
- Frontend pages: `src/chat_project/web_static`
- Utilities & models: `src/chat_project/models` and tests in `tests/unit`
- Data files: `src/chat_project/data/json`

Quick start (Windows)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure secrets

- Add `credentials.json` and `token.json` into `src/chat_project/data/json/` as needed (these files are gitignored).

3. Run the servers

- Start authentication server (if required):

```powershell
python src\chat_project\api\auth\server.py
```

- Start messaging server (if required):

```powershell
python src\chat_project\api\messages\server.py
```

4. Open the frontend pages in a browser from `src/chat_project/web_static/` (e.g., `src/chat_project/web_static/login/login.html`).

Repository layout

- `src/PYTHON/SERVER` — server components for auth and messaging
- `src/PYTHON/WEB` — static frontend (login, signup, otp)
- `src/PYTHON/Utils` — helper modules and tests
- `src/DATA/JSON` — JSON data & tokens

Where to get help

- Check `docs/ARCHITECTURE.md` for component descriptions.

License

See `LICENSE` in repository root.
