from flask import Flask
app = Flask(__name__)
from app import routes
from app import database_sqlite
