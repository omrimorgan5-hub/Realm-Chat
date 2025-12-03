import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import random
from datetime import datetime


app = Flask(__name__)

CORS(app)

