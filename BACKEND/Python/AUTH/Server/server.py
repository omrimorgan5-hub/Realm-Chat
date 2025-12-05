import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from datetime import datetime
import functions
from functions import signup,load_data,login,verify_otp,save_data,send_email  



app = Flask(__name__)
CORS(app)  # Allow frontend on different port/origin\

ACCOUNTS_FILE = 'accounts.json'


app.add_url_rule('/signup', view_func=signup ,methods=['POST'])
app.add_url_rule('/login', view_func=login ,methods=['POST'])
app.add_url_rule('/verify-otp', view_func=verify_otp ,methods=['POST'])


if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)