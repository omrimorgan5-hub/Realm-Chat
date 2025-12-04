import json
import random
import os
import re
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime

ACCOUNTS_FILE = 'accounts.json'

# functions for general use.
def gen_otp():
    random.randint(100000, 999999)

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

    # Check for duplicate username
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

def send_email():
    pass

def verify_otp():
    pass
    