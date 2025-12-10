import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import sys
from datetime import datetime
import functions
from functions import *  

def server():

    app = Flask(__name__)
    CORS(app) 
    
    # 2. Configure Flask-SQLAlchemy on the main app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    
    # 3. Associate the imported 'db' object with this app instance
    db.init_app(app)

    # 4. Create the database tables if they don't exist (CRITICAL STEP)
    with app.app_context():
        db.create_all()

    # 5. Add URL Rules
    app.add_url_rule('/signup', view_func=signup ,methods=['POST'])
    app.add_url_rule('/login', view_func=login ,methods=['POST'])
    app.add_url_rule('/verify-otp', view_func=verify_otp ,methods=['POST'])

    print("Server running at http://0.0.0.0:5000")
    # Note: Use 'app.run()' for development, or a production server like Waitress/Gunicorn for deployment
    app.run(debug=True, host='0.0.0.0', port=5000)

