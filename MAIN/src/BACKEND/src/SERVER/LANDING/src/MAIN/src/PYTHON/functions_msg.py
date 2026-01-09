import random
import os
import uuid
import threading
import re
from flask import Flask, request, jsonify, make_response # Flask items are needed for request/jsonify
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timedelta
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

temp_app_for_db = Flask(__name__)
temp_app_for_db.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
temp_app_for_db.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(temp_app_for_db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    sender = db.Column(db.String(80), unique=False, nullable=False)
    recipitent = db.Column(db.String(120), unique=False, nullable=False)
    msg_data = db.Column(db.String(500), unique=False, nullable=False)
    time_sent = db.Column(db.DateTime, default=datetime.now, nullable=False)
    msg_id = db.Column(db.String(36), unique=True, nullable=False)
    
    
    def __repr__(self):
        return f'<User {self.sender}>'


def send_message_realm():

    if request.method == 'OPTIONS':
        response = make_response(jsonify({"status": "ok"}), 200)
        # Force the connection to close so the POST can start fresh
        response.headers["Connection"] = "close"
        return response

    def gen_id():
        id = str(uuid.uuid4())
        return id
    
    
    info_user = request.get_json()
    
    if not info_user:
        return jsonify({"message": "No data provided."}), 400
        
        
    sender = info_user.get("sender")
    recipitent = info_user.get("recipitent")
    msg_data = info_user.get("message")
    
    if len(msg_data) <= 0 or len(msg_data) > 500:
        return jsonify({"message": "Message is to long or small must be 1-500 chars."}), 400
     
    msg_id = gen_id()
    new_msg = User(
        sender=sender,
        recipitent=recipitent,
        msg_data=msg_data,
        msg_id=msg_id
        
    )
    
    db.session.add(new_msg)
    db.session.commit()
    
    print(f"sent message {msg_id}.")

    return jsonify({"message": "Success."}), 201
    
    
    
    
    