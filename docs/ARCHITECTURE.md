# Architecture

Overview

Realm is organized into a small set of concerns:

- Authentication: `src/chat_project/api/auth/server.py` handles authentication flows and token management (handlers live in `src/chat_project/api/auth/handlers.py`).
- Messaging: `src/chat_project/api/messages/server.py` implements message routing/handling (handlers live in `src/chat_project/api/messages/handlers.py`).
- Frontend: static pages under `src/chat_project/web_static` provide login, signup and OTP flows.
- Models & Utilities: `src/chat_project/models` contains SQLAlchemy models and backend helpers.
- Data: `src/chat_project/data/json` stores local JSON credentials and tokens; DB files live under `src/chat_project/data/db`.

Component responsibilities

- server_auth.py
  - Validate credentials
  - Issue/validate tokens

- server_msg.py
  - Receive messages from clients
  - Route and store messages (and forward to DB)

- Frontend (WEB)
  - Simple static UI, uses local JS to call backend endpoints

Data flow

1. Client submits login/signup from frontend
2. Frontend calls auth server endpoints
3. Auth server validates and returns tokens saved as `token.json`
4. Messaging server accepts messages authenticated with tokens

Notes

- The project currently uses JSON files for small-scale state; a SQL database is noted in `docs/Info.md` for planned persistence.
