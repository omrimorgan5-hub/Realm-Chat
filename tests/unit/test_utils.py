import random
import os
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
import sys


from chat_project.api.auth.handlers import gen_otp, hash_password


def test_gen_otp():
    otp = gen_otp()
    assert isinstance(otp, str)
    assert len(otp) == 6
    assert otp.isdigit()


def test_hash_password():
    h = hash_password("abc123")
    assert isinstance(h, str)
    assert len(h) == 64


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Secrets are not required for unit tests. For integration tests, place
# `credentials.json` and `token.json` under `src/chat_project/data/json/` or
# set credentials via environment variables.







