import random
import os
import sys
import threading
import re
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


# Package imports (models and helpers)
from chat_project.models.models import db, User_auth, backend_auth

auth_backend = backend_auth()


# --- GLOBAL SETUP ---


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
Credentials_json = os.path.join(BASE_DIR, "data", "json", "credentials.json")
Token_json = os.path.join(BASE_DIR, "data", "json", "token.json")
# --- DATABASE MODEL ---



# --- UTILITY FUNCTIONS ---


def gen_otp(): # has passed tests
    """Generates a random 6-digit string OTP."""
    return str(random.randint(100000, 999999)) 



def hash_password(password: str) -> str: # has passed tests
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()



def gmail_authenticate(): # has passed tests
    """Authenticates with Gmail API for sending emails."""
    # This logic remains the same
    creds = None
    if os.path.exists(Token_json):
        creds = Credentials.from_authorized_user_file(Token_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(Credentials_json, SCOPES)
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)





def send_email(recipient, otp, username): # has passed tests
    """Sends the OTP code via Gmail API."""
    print("Sending")
    service = gmail_authenticate()
    message = MIMEText(f"hello {username}! Your OTP is: {otp}")
    message['to'] = recipient
    message['subject'] = "Your OTP Code"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw}).execute()
    print(f"OTP {otp} sent to {username}")



# --- FLASK VIEW FUNCTIONS (ROUTES) ---

"""  
signup function currently passed all tests prepared-
for next steps of development.
"""


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

    # Validation
    if len(password) < 8 or len(password) > 64:
        return jsonify({"message": "Password must be between 8 and 64 characters."}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400
    try:
        datetime.fromisoformat(birthday)
    except ValueError:
        return jsonify({"message": "Invalid birthday format."}), 400
    
    # Check for duplicate using SQLAlchemy
    # These calls now work because of the 'with current_app.app_context()' we added to backend_auth


    if auth_backend.get_username(username=username):
        return jsonify({"message": "Username already taken."}), 409
    if auth_backend.get_email(email=email):
        return jsonify({"message": "Email already registered."}), 409

    hashed_password = hash_password(password)
    otp_code = gen_otp()
    otp_expiration = datetime.now() + timedelta(minutes=10)

    # UPDATED: Use User_auth instead of User
    new_user = User_auth(
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

    # FIXED: Added () to .start()
    email_thread = threading.Thread(
        target=send_email,
        args=(email, otp_code, username)
    )
    email_thread.start() # Added parentheses here
    
    print(f"New user registered: {username}")

    return jsonify({"message": "Signup successful! OTP sent."}), 200



"""  
login function currently passed all tests prepared-
for next steps of development.
"""


def login(): # has passed tests
    """Handles user login authentication and checks for verification status."""
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No data provided."}), 400

    username = info_user.get('username')
    password = info_user.get('password')

    if not all([username, password]):
        return jsonify({"message": "All fields are required."}), 400

    hashed_password = hash_password(password)
    
    user = auth_backend.get_username(username=username)

    if user and auth_backend.get_password(password=hashed_password):
        if not auth_backend.user.get_is_verified:
             return jsonify({"message": "Account not verified. Please verify email."}), 403 
        
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid username or password."}), 401





"""
verify otp function used for account verification-
work in progress current version is to be reworked due to issues-
internaly.

UPDATE: I have fixed core issues will continue to work internally.
"""



def verify_otp(): # hasn't passed tests 2/3 passed
    """Handles OTP submission, validates the code, and verifies the user."""
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No Data provided."}), 400
    
    otp_entered = info_user.get("otp")
    username = info_user.get("username")
    
    if not all([otp_entered, username]):
        return jsonify({"message": "Username and OTP are required."}), 400
    
    user = auth_backend.get_username(username=username)
    
    if not user:
        return jsonify({"message": "Invalid username."}), 401
    
    if user.is_verified:
        return jsonify({"message": "Account already verified."}), 409

    # 1. Check for expiration
    if user.otp_expires_at < datetime.utcnow():

        otp_code = gen_otp()

        email_thread = threading.Thread(
        target=send_email,
        args=(user.email, otp_code, username)
        )

        email_thread.start()

        user.otp_code = otp_code
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "OTP has expired. please check your email"}), 401
    
    if user.otp_code is None:
        return jsonify({"message": "OTP Entered is either expired or is invalid you may also already be verified."}), 409

    # 2. Check for code match
    if user.otp_code == str(otp_entered):


        user.is_verified=True
        user.otp_code=None
        user.otp_expires_at=None
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "OTP verified, continue."}), 200
    else:
        return jsonify({"message": "Invalid OTP."}), 401











