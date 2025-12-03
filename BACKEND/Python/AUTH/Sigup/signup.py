import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend on different port/origin

ACCOUNTS_FILE = 'accounts.json'

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

@app.route('/signup', methods=['POST'])
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

    # Load existing users
    users = load_data()

    # Check for duplicate username
    if any(user['username'] == username for user in users):
        return jsonify({"message": "Username already taken."}), 409

    # Hash password before saving
    hashed_password = hash_password(password)

    new_user = {
        "username": username,
        "password": hashed_password,  # Never store plain passwords!
        "birthday": birthday,
        "display_name": display_name,
        "email": email,
        "created_at": datetime.now().isoformat()
    }

    users.append(new_user)
    save_data(users)

    print(f"New user registered: {username}")
    return jsonify({"message": "Signup successful!"}), 201

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)