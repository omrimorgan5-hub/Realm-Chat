import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Define the project root once
BASE_DIR = Path(__file__).resolve().parent

# 2. Explicitly load the .env from the root
load_dotenv(BASE_DIR / ".env")

class Config:
    # 3. Use 'or ""' to prevent the NoneType error if .env is missing a key
    TOKEN_JSON = (BASE_DIR / (os.getenv("Token_json") or "")).resolve()
    CREDENTIALS_JSON = (BASE_DIR / (os.getenv("Credentials_json") or "")).resolve()
    
    # SQLAlchemy absolute path (3 slashes for Windows: sqlite:///C:/...)
    DB_AUTH = (BASE_DIR / (os.getenv("DB_AUTH_PATH") or "")).resolve()
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_AUTH.as_posix()}"
    
    DB_MSG = (BASE_DIR / (os.getenv("DB_MESSAGE_PATH") or "")).resolve()
    SQLALCHEMY_BINDS = {
        "auth": f"sqlite:///{DB_AUTH.as_posix()}",
        "msg": f"sqlite:///{DB_MSG.as_posix()}"
    }

@staticmethod
def init_app():
    Config.AUTH_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    Config.MSG_DB_PATH.parent.mkdir(parents=True, exist_ok=True)