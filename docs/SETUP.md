# Setup

This document explains how to prepare a development environment for Chat-Project on Windows.

Prerequisites

- Python 3.10+ (or the version used in `requirements.txt`)
- Git

Steps

1. Clone the repository:

```powershell
git clone <repo-url>
cd Chat-Project
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Prepare credentials and tokens

- Copy `credentials.json` and `token.json` into `src/DATA/JSON/` or ensure `credentials.json` in root is configured.

5. Environment variables (optional)

- If your deployment requires environment variables (e.g., DB connection strings), set them in your shell or use a `.env` loader if added later.

Run smoke test

- Run the included test script to verify utilities:

```powershell
python src/PYTHON/Utils/TEST/test.py
```

Notes

- If you use PowerShell, ensure script execution policy allows activating the virtualenv (`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`).
