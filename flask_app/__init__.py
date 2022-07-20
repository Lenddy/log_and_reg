from flask import Flask,session
app = Flask(__name__)
app.secret_key = "secret"

db = "log_registration_schema"