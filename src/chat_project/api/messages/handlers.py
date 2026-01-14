import random
import os
import sys
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


# Package imports (models and helpers)
try:
    from chat_project.models.models import db, User_msg, backend_msg
except ModuleNotFoundError:
    # Running without package context: add project 'src' to sys.path and retry
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from chat_project.models.models import db, User_msg, backend_msg



msg_backend = backend_msg()



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
    
    
