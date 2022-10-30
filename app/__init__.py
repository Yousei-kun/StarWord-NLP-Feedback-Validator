from flask import Flask

app = Flask(__name__)
app.secret_key = 'starword'

from app import routes