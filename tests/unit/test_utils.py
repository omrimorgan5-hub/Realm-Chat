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


# Use package imports for test helper functions
from chat_project.api.auth.handlers import send_email

send_email("omrimorgan5@gmail.com", "232323", "Shadow680")


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


Credentials_json = 'C:/Users/Omri.Morgan02/Downloads/Chat-Project/MAIN/ASSETS/JSON/credentials.json'
Token_json = "C:/Users/Omri.Morgan02/Downloads/Chat-Project/MAIN/ASSETS/JSON/token.json"







