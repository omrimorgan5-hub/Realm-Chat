# Realm Chat 🗨️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Status](https://img.shields.io/badge/status-building-important)](https://github.com/omrimorgan5-hub/Realm-Chat)

An evolving real-time chat application. This repo contains a lightweight Python backend, simple static frontend pages, and utilities used during development.

Key points

- **Auth:** e-mail based authentication and token handling
- **Realtime:** WebSocket-powered messaging (backend + frontend)
- **Storage:** JSON file store used in development; PostgreSQL migration planned

Tech roadmap (summary)

- Frontend: JavaScript → TypeScript
- Backend: Flask (MVP) → Django/Django-Channels (scale)
- Database: JSON files → PostgreSQL
- Deploy: Local development → Docker / cloud hosting

Quick start (local dev)

1. Clone repository

```powershell
git clone <repo-url>
cd Chat-Project
```

2. Create and activate a Python virtual environment

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

4. Configure credentials

- Ensure `credentials.json` and `token.json` are present in `src/chat_project/data/json/` or configured according to your environment (these files are intentionally gitignored).

5. Run servers (examples)

```powershell
python src\chat_project\api\auth\server.py
python src\chat_project\api\messages\server.py
```

Open the frontend pages in a browser from `src/chat_project/web_static/` (for example `src/chat_project/web_static/login/login.html`).

Repository layout (top-level)

- `src/` — application source (server, web, utils)
- `docs/` — project documentation
- `requirements.txt` — Python deps
- `LICENSE` — project license

Contributing

- Fork the repository, create a branch `feature/your-change`, make focused commits, and open a pull request.
- Run tests before submitting: set `PYTHONPATH=src` and run `python -m pytest` (or use your test runner of choice).

License

MIT © Omri Morgan

Need help or want a PR to be reviewed? Open an issue or create a pull request on GitHub.
