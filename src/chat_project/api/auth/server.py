import os
import sys
from flask import Flask
from flask_cors import CORS

# Package imports
try:
    from chat_project.models.models import db
    from chat_project.api.auth import handlers as auth_funcs
except ModuleNotFoundError:
    # Running without package context: add project 'src' to sys.path and retry
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from chat_project.models.models import db
    from chat_project.api.auth import handlers as auth_funcs




from chat_project.models.models import db
from chat_project.api.auth import handlers as auth_funcs

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
db_auth_path = os.getenv("DB_AUTH_PATH")
db_msg_path = os.getenv("DB_MESSAGE_PATH")

def server():
    # Adding 'global db' ensures the function looks outside for the variable
    global db 
    
    app = Flask(__name__)
    CORS(app) 
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_auth_path}'
    app.config['SQLALCHEMY_BINDS'] = {
        'auth': f'sqlite:///{db_auth_path}',
        'msg':  f'sqlite:///{db_msg_path}'
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. Initialize the app


    db.init_app(app)

    # Functions are imported from package handlers
    from chat_project.api.auth.handlers import signup, login, verify_otp

    with app.app_context():
        db.create_all()

    # URL Rules
    app.add_url_rule('/signup', view_func=signup, methods=['POST'])
    app.add_url_rule('/login', view_func=login, methods=['POST'])
    app.add_url_rule('/verify-otp', view_func=verify_otp, methods=['POST'])

    print("Server running at http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server()