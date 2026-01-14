import os
import sys
from flask import Flask
from flask_cors import CORS

# Package imports
from chat_project.models.models import db
from chat_project.api.messages import handlers as msg_funcs

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
db_auth_path = os.path.join(BASE_DIR, "src", "chat_project", "data", "db", "accounts.db")
db_msg_path = os.path.join(BASE_DIR, "src", "chat_project", "data", "db", "messages.db")

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
    from chat_project.api.messages.handlers import send_message_realm

    with app.app_context():
        db.create_all()

    # URL Rules
    app.add_url_rule('/message', view_func=send_message_realm, methods=['POST'])


    print("Server running at http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server()