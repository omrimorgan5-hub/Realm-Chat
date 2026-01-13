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

- Ensure `credentials.json` and `token.json` are present in `src/DATA/JSON/` or configured according to your environment.

5. Run servers (examples)

```powershell
python src/PYTHON/SERVER/server_auth.py
python src/PYTHON/SERVER/server_msg.py
```

Open the frontend pages in a browser from `src/PYTHON/WEB/` (for example `LOGIN/login.html`).

Repository layout (top-level)

- `src/` — application source (server, web, utils)
- `docs/` — project documentation
- `requirements.txt` — Python deps
- `LICENSE` — project license

Contributing

- Fork the repository, create a branch `feature/your-change`, make focused commits, and open a pull request.
- Run tests before submitting: `python src/PYTHON/Utils/TEST/test.py`

License

MIT © Omri Morgan

Need help or want a PR to be reviewed? Open an issue or create a pull request on GitHub.
