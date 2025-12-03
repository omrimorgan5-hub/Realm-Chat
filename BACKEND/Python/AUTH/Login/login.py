import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend on different port/origin

ACCOUNTS_FILE = "accounts.json"


# -------------------- Utility Functions --------------------

def load_data():
    """Load users from accounts.json, return as list of dicts."""
    if not os.path.exists(ACCOUNTS_FILE) or os.stat(ACCOUNTS_FILE).st_size == 0:
        return []
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("JSON corrupted, starting fresh.")
        return []


def save_data(data):
    """Save list of user dicts to accounts.json."""
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------- Routes --------------------



@app.route('/login', methods=['POST'])
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
    print(users)

    print("Login attempt:", username, hashed_password)

    # Check credentials
    for user in users:
        print("Stored:", user.get("username"), user.get("password"))
        if user.get("username") == username and user.get("password") == hashed_password:
            return jsonify({"message": "Login successful!"}), 200

    return jsonify({"message": "Invalid username or password."}), 401


# -------------------- Run Server --------------------

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)
