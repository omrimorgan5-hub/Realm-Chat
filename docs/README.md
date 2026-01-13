# Chat-Project

Short description

A lightweight chat project with a Python backend and static web frontend. This repository contains authentication and messaging modules, simple web pages for login/signup/OTP, and utilities for testing.

Quick links

- Project root: `.`
- Server code: `src/PYTHON/SERVER`
- Frontend pages: `src/PYTHON/WEB`
- Utilities & tests: `src/PYTHON/Utils`
- Data files: `src/DATA/JSON`

Quick start (Windows)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure secrets

- Add `credentials.json` and `token.json` into `src/DATA/JSON/` as needed.

3. Run the servers

- Start authentication server (if required):

```powershell
python src/PYTHON/SERVER/server_auth.py
```

- Start messaging server (if required):

```powershell
python src/PYTHON/SERVER/server_msg.py
```

4. Open the frontend pages in a browser from `src/PYTHON/WEB/` (e.g., `LOGIN/login.html`).

Repository layout

- `src/PYTHON/SERVER` — server components for auth and messaging
- `src/PYTHON/WEB` — static frontend (login, signup, otp)
- `src/PYTHON/Utils` — helper modules and tests
- `src/DATA/JSON` — JSON data & tokens

Where to get help

- Check `docs/ARCHITECTURE.md` for component descriptions.

License

See `LICENSE` in repository root.
