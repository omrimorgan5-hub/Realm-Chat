Reorganization summary

What changed
- Project now uses a proper package layout under `src/chat_project`.
- Servers and handlers moved to `src/chat_project/api/*`.
- Models moved to `src/chat_project/models/models.py`.
- Static frontend assets moved to `src/chat_project/web_static/*`.
- Data files live under `src/chat_project/data/*` (JSON and DB).
- Tests moved to `tests/unit/` and use pytest by default.

How to run tests
- From PowerShell:
  $env:PYTHONPATH='src'; python -m pytest

How to run servers (example)
- Start auth server:
  python src\chat_project\api\auth\server.py
- Start messages server:
  python src\chat_project\api\messages\server.py

Notes
- `credentials.json` and `token.json` are intentionally ignored by git; provide them in `src/chat_project/data/json/` for Gmail features.
- This refactor primarily reorganizes files and updates imports; code behavior was not changed except paths and doc updates.
