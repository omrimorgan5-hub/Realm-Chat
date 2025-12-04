import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime
from Python.AUTH.functions.functions import load_data, save_data, hash_password, signup, login

app = Flask(__name__)
CORS(app)  # Allow frontend on different port/origin

ACCOUNTS_FILE = 'accounts.json'


app.add_url_rule('/signup', view_func=signup ,methods=['POST'])
app.add_url_rule('/login', view_func=login ,methods=['POST'])


if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)