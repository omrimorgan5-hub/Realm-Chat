import os
import sys
from flask import Flask
from flask_cors import CORS

# 1. Fix pathing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# 2. Import 'db' specifically
from src.PYTHON.Utils.utils_classes import db

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
db_auth_path = os.path.join(BASE_DIR, "src", "DATA", "DB", "accounts.db")
db_msg_path = os.path.join(BASE_DIR, "src", "DATA", "DB", "messages.db")

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

    # 4. NOW import the functions (Delayed import to prevent RuntimeError)
    import src.PYTHON.Utils.functions_msg as msg_funcs

    with app.app_context():
        db.create_all()

    # URL Rules
    app.add_url_rule('/signup', view_func=msg_funcs.send_message_realm, methods=['POST'])


    print("Server running at http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server()