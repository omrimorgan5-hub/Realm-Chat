import json
import random
import os
import re
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

ACCOUNTS_FILE = 'accounts.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# functions for general use.
def gen_otp():
    return random.randint(100000, 999999)

def load_data():
    if not os.path.exists(ACCOUNTS_FILE) or os.stat(ACCOUNTS_FILE).st_size == 0:
        return []
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("JSON corrupted, starting fresh.")
        return []

def save_data(data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)



def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# signup function.
def signup():


    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No data provided."}), 400

    username = info_user.get('username')
    password = info_user.get('password')
    birthday = info_user.get('birthday')
    display_name = info_user.get('display_name')
    email = info_user.get('email')

    if not all([username, password, birthday, display_name]):
        return jsonify({"message": "All fields are required."}), 400

    if len(password) < 8 or len(password) > 64:
        return jsonify({"message": "Password must be between 8 and 64 characters."}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400

    try:
        datetime.fromisoformat(birthday)
    except ValueError:
        return jsonify({"message": "Invalid birthday format."}), 400

    # Load existing users
    users = load_data()

    # Check for duplicate username and email
    if any(user['username'] == username for user in users):
        return jsonify({"message": "Username already taken."}), 409
    if any(user['email'] == email for user in users):
        return jsonify({"message": "Email already registered."}), 409


    # Hash password before saving
    hashed_password = hash_password(password)

    new_user = {
        "username": username,
        "password": hashed_password,  # Never store plain passwords!
        "birthday": birthday,
        "display_name": display_name,
        "email": email,
        "is_verified": False,
        "created_at": datetime.now().isoformat()
    }

    otp = gen_otp()
    send_email(email, otp)
    new_user["otp"] = otp

    users.append(new_user)
    save_data(users)

    print(f"New user registered: {username}")
    return jsonify({"message": "Signup successful!"}), 201

# login function.

def login():
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No data provided."}), 400

    username = info_user.get('username')
    password = info_user.get('password')

    if not all([username, password]):
        return jsonify({"message": "All fields are required."}), 400

    users = load_data()
    hashed_password = hash_password(password)
    
    # Check credentials
    for user in users:
        if user.get("username") == username and user.get("password") == hashed_password:
            return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid username or password."}), 401


def verify_otp():
    info_user = request.get_json()

    if not info_user:
        return jsonify({"message": "No Data provided."}), 400
    
    otp_entered = str(info_user.get("otp")).strip()
    username = info_user.get("username")

    users = load_data()
    updated = False

    for user in users:
        if user.get("username") == username:
            if user.get("is_verified"):
                return jsonify({"message": "OTP already verified."}), 200
            elif str(user.get("otp")) == str(otp_entered):
                user.pop("otp", None)
                user["is_verified"] = True
                updated = True
                break

    if updated:
        save_data(users)  # save the whole list back
        return jsonify({"message": "OTP verified, continue."}), 200
    else:
        return jsonify({"message": "Invalid OTP."}), 401
    
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
Credentials_json = 'credentials.json'

def gmail_authenticate():
    creds = None
    # Load saved token if it exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid creds, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(Credentials_json, SCOPES)
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")

        # Save token for next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(recipient, otp):
    service = gmail_authenticate()

    message = MIMEText(f"Your OTP is: {otp}")
    message['to'] = recipient
    message['subject'] = "Your OTP Code"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw}).execute()
    print(f"OTP {otp} sent to {recipient}")
