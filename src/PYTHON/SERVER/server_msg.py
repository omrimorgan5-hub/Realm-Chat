import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import src.PYTHON.Utils.utils_classes
from src.PYTHON.Utils.utils_classes import *
import src.PYTHON.Utils.functions_msg
from src.PYTHON.Utils.functions_msg import *

db_msg_path = r'C:\Users\Omri.Morgan02\Downloads\Chat-Project\src\DATA\DB\messages.db'
db_auth_path = r'C:\Users\Omri.Morgan02\Downloads\Chat-Project\src\DATA\DB\accounts.db'




def server():

    app = Flask(__name__)
    CORS(messaging) 
    
    # 2. Configure Flask-SQLAlchemy on the main app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_msg_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
    'auth': f'sqlite:///{db_auth_path}',
    'msg':  f'sqlite:///{db_msg_path}'
}
    
    # 3. Associate the imported 'db' object with this app instance
    db.init_app(app)

    # 4. Create the database tables if they don't exist (CRITICAL STEP)
    with app.app_context():
        db.create_all()

    # 5. Add URL Rules
    app.add_url_rule('/send_msg', view_func=send_message_realm ,methods=['POST'])
    

    print("Server running at http://0.0.0.0:5001")
    backend_msg = backend_msg()
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == "__main__":
    server()