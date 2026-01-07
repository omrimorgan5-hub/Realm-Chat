import json
import random
import os
import threading
import re
import smtplib
from flask import Flask, request, jsonify # Flask items are needed for request/jsonify
from flask_sqlalchemy import SQLAlchemy 
import hashlib
from datetime import datetime, timedelta 
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# --- GLOBAL SETUP ---

# NOTE: The Flask app object must be defined *once* in your server file (e.g., server.py)
# and passed or imported here. For simplicity in this functions file, 
# we'll assume the Flask app is available for SQLAlchemy config.

# We define a temporary Flask app instance just for SQLAlchemy configuration
# This instance will be configured to use SQLite.
temp_app_for_db = Flask(__name__)
temp_app_for_db.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
temp_app_for_db.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(temp_app_for_db)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
Credentials_json = 'credentials.json'

# --- DATABASE MODEL ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    birthday = db.Column(db.String(10), nullable=False)
    display_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    is_verified = db.Column(db.Boolean, default=False)
    otp_code = db.Column(db.String(6), nullable=True) 
    otp_expires_at = db.Column(db.DateTime, nullable=True) 
    
    def __repr__(self):
        return f'<User {self.username}>'

# --- UTILITY FUNCTIONS ---

def gen_otp():
    """Generates a random 6-digit string OTP."""
    return str(random.randint(100000, 999999)) 

def hash_password(password: str) -> str:
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def gmail_authenticate():
    """Authenticates with Gmail API for sending emails."""
    # This logic remains the same
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(Credentials_json, SCOPES)
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(recipient, otp, username):
    """Sends the OTP code via Gmail API."""
    service = gmail_authenticate()
    message = MIMEText(f"hello {username}! Your OTP is: {otp}")
    message['to'] = recipient
    message['subject'] = "Your OTP Code"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw}).execute()
    print(f"OTP {otp} sent to {recipient}")

# --- FLASK VIEW FUNCTIONS (ROUTES) ---

def signup():
    """Handles new user registration, storing data in SQLite."""
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No data provided."}), 400

    username = info_user.get('username')
    password = info_user.get('password')
    birthday = info_user.get('birthday')
    display_name = info_user.get('display_name')
    email = info_user.get('email')

    if not all([username, password, birthday, display_name, email]):
        return jsonify({"message": "All fields are required."}), 400

    # Validation (Remains the same)
    if len(password) < 8 or len(password) > 64:
        return jsonify({"message": "Password must be between 8 and 64 characters."}, 400)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400
    try:
        datetime.fromisoformat(birthday)
    except ValueError:
        return jsonify({"message": "Invalid birthday format."}), 400
    
    # Check for duplicate using SQLAlchemy
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already taken."}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered."}), 409
    


    hashed_password = hash_password(password)
    otp_code = gen_otp()
    otp_expiration = datetime.utcnow() + timedelta(minutes=10)

    new_user = User(
        password=hashed_password,
        birthday=birthday,
        username=username,
        display_name=display_name,
        email=email,
        otp_code=otp_code,
        otp_expires_at=otp_expiration
        )

    db.session.add(new_user)
    db.session.commit() 

    email_thread = threading.Thread(
        target=send_email,
        args=(email, otp_code, username)
    )
    email_thread.start
    
    print(f"New user registered: {username}")
    print(f"Sent {otp_code} to new user {username}")
    return jsonify({"message": "Signup successful! OTP sent."}),200


def login():
    """Handles user login authentication and checks for verification status."""
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No data provided."}), 400

    username = info_user.get('username')
    password = info_user.get('password')

    if not all([username, password]):
        return jsonify({"message": "All fields are required."}), 400

    hashed_password = hash_password(password)
    
    user = User.query.filter_by(username=username).first()

    if user and user.password == hashed_password:
        if not user.is_verified:
             return jsonify({"message": "Account not verified. Please verify email."}), 403 
        
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid username or password."}), 401


def verify_otp():
    """Handles OTP submission, validates the code, and verifies the user."""
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No Data provided."}), 400
    
    otp_entered = info_user.get("otp")
    username = info_user.get("username")
    
    if not all([otp_entered, username]):
        return jsonify({"message": "Username and OTP are required."}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"message": "Invalid username."}), 401
    
    if user.is_verified == True:
        return jsonify({"message": "Account already verified."}), 409

    # 1. Check for expiration
    if user.otp_expires_at < datetime.utcnow():
        # Clean up expired fields
        user.otp_code = None
        user.otp_expires_at = None
        db.session.commit()
        email = User.query.filter_by(email=email).first()
        print(email)
        otp_code = gen_otp()
        send_email(email, otp, username)
        db.session.commit()
        return jsonify({"message": "OTP has expired. You have been sent a new code."}, 401)
    
    if user.otp_code == None:
        return jsonify({"message": "OTP Entered is either expired or is invalid you may also already be verified."}, 409)

    # 2. Check for code match
    if user.otp_code == str(otp_entered):
        # Update user status and clear OTP fields
        user.is_verified = True
        user.otp_code = None
        user.otp_expires_at = None
        db.session.commit()
        
        return jsonify({"message": "OTP verified, continue."}), 200
    else:
        return jsonify({"message": "Invalid OTP."}), 401

def send_message():
    pass