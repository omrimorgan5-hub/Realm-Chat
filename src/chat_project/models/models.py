import random
import os
import sys
import threading
import re
from flask import Flask, request, jsonify, current_app # Flask items are needed for request/jsonify
from flask_sqlalchemy import SQLAlchemy 
import hashlib
from datetime import datetime, timedelta
import base64

# binds (use project-relative paths)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_auth_path = os.path.join(BASE_DIR, "data", "db", "accounts.db")
db_msg_path = os.path.join(BASE_DIR, "data", "db", "messages.db")



# User_auth class



db = SQLAlchemy()

class User_auth(db.Model):
    __bind_key__ = 'auth'

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
    birthday = db.Column(db.String(10), nullable=False)
    display_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    is_verified = db.Column(db.Boolean, default=False)
    otp_code = db.Column(db.String(6), nullable=True) 
    otp_expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'



# user_msg class



class User_msg(db.Model):
    __bind_key__ = 'msg'

    id = db.Column(db.Integer, primary_key=True) 
    sender = db.Column(db.String(80), unique=False, nullable=False)
    recipitent = db.Column(db.String(120), unique=False, nullable=False)

    msg_data = db.Column(db.String(500), unique=False, nullable=False)
    time_sent = db.Column(db.DateTime, default=datetime.now, nullable=False)
    msg_id = db.Column(db.String(36), unique=True, nullable=False)
    
    
    def __repr__(self):
        return f'<User {self.sender}>'



# backend_auth class


class backend_auth:

    def get_username(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_password(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_otp(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_email(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_id(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_created_at(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first() 

    def get_birthday(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_otp_expires_at(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_is_verified(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

# backend_msg class


class backend_msg:
    def get_sender(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_rescipient(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_msg_id(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_msg_data(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_id(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()

    def get_time_sent_at(self, **kwargs):
        with current_app.app_context():
            return User_auth.query.filter_by(**kwargs).first()