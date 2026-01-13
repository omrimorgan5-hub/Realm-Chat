# Architecture

Overview

Realm is organized into a small set of concerns:

- Authentication: `src/PYTHON/SERVER/server_auth.py` handles authentication flows and token management.
- Messaging: `src/PYTHON/SERVER/server_msg.py` implements message routing/handling.
- Frontend: static pages under `src/PYTHON/WEB` provide login, signup and OTP flows.
- Utilities: `src/PYTHON/Utils` contains helper functions and test code.
- Data: `src/DATA/JSON` stores local JSON credentials and tokens.

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
