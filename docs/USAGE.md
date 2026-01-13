# Usage

How to run the project components and use the app locally.

Running servers

- Authentication server:

```powershell
python src/PYTHON/SERVER/server_auth.py
```

- Messaging server:

```powershell
python src/PYTHON/SERVER/server_msg.py
```

Accessing the frontend

- Open the static HTML pages in `src/PYTHON/WEB/` with a browser, for example:
  - `src/PYTHON/WEB/LOGIN/login.html`
  - `src/PYTHON/WEB/SIGNUP/signup.html`
  - `src/PYTHON/WEB/OTP/otp_auth.html`

Testing

- Run the unit/util test in `src/PYTHON/Utils/TEST/test.py`:

```powershell
python src/PYTHON/Utils/TEST/test.py
```

Logs and troubleshooting

- Check console output where the servers run for error messages.
- Ensure `credentials.json` and `token.json` are in place when starting servers.
