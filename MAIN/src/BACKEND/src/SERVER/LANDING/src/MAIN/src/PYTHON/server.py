import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import sys
from datetime import datetime
import functions_msg
from functions_msg import *  

def server():

    messaging = Flask(__name__)
    CORS(messaging, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type"]) 
    
    # 2. Configure Flask-SQLAlchemy on the main app instance
    messaging.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
    messaging.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    # 3. Associate the imported 'db' object with this app instance
    db.init_app(messaging)

    # 4. Create the database tables if they don't exist (CRITICAL STEP)
    with messaging.app_context():
        db.create_all()

    # 5. Add URL Rules
    messaging.add_url_rule('/send_msg', view_func=send_message_realm ,methods=['POST', 'OPTIONS'])
    

    print("Server running at http://0.0.0.0:5000")

    messaging.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

