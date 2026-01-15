import os
import sys
from flask import Flask
from flask_cors import CORS
from config import Config  # Your source of truth


# Package imports with path fix
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chat_project.models.models import db
# Import views/handlers
from chat_project.api.messages.handlers import send_message_realm

def server():
    app = Flask(__name__)
    CORS(app) 
    
    # 1. Load everything (DB paths, Secrets, etc.) from the Config class
    app.config.from_object(Config)

    print(f"DEBUG: Using DB URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"DEBUG: Current Working Directory: {os.getcwd()}")
    # 2. Initialize DB
    db.init_app(app)

    # 3. Create tables using the paths defined in Config
    with app.app_context():
        db.create_all()

    # 4. URL Rules
    app.add_url_rule('/message', view_func=send_message_realm, methods=['POST'])

    print("Server running at http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server()