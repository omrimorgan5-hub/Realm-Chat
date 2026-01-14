# Usage

How to run the project components and use the app locally.

Running servers

- Authentication server:

```powershell
python src\chat_project\api\auth\server.py
```

- Messaging server:

```powershell
python src\chat_project\api\messages\server.py
```

Accessing the frontend

- Open the static HTML pages in `src/chat_project/web_static/` with a browser, for example:
  - `src/chat_project/web_static/login/login.html`
  - `src/chat_project/web_static/signup/signup.html`
  - `src/chat_project/web_static/otp/otp_auth.html`

Testing

- Run the unit tests (set PYTHONPATH to `src`):

```powershell
$env:PYTHONPATH='src'; python -m pytest
```

Logs and troubleshooting

- Check console output where the servers run for error messages.
- Ensure `credentials.json` and `token.json` are in place when starting servers.
