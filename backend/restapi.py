from flask import Flask, request, jsonify
from sql import DBconnection, execute_read_query, execute_update_query
from creds import Creds
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection
con = DBconnection(Creds.hostname, Creds.username, Creds.password, Creds.database)