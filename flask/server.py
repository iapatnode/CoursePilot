from flask import Flask, request, render_template, redirect, session, Response
from flask_cors import CORS
import os
import re, json
from mysql.connector import connect, Error

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.urandom(32)

#Settings for testing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Credentails for database connection
"""scriptdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptdir, "config.json")) as text:
    config = json.load(text)

#Connects to server and creates database
def create_db():
    try:
        with connect(host=config.get('host'), user=config.get('username'), password=config.get('password')) as conn:
            with conn.cursor() as cursor:
                cursor.execute("create database if not exists course_pilot")  
    except Error as error:
        print(error)

#Establishes connection to database
def connection():
    try:
        with connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database="course_pilot") as conn:
            return conn
    except Error as error:
        print(error)

#Creating and initializing the database
def init_db():
    try:
        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("select * from Student")

    except Exception as exception:
        print("database not found")
        print(exception)
        #TODO: create tables and fill with dummy data

#Creates Course Pilot database and fills it with tables and data when application is opened
create_db()
init_db()"""


@app.route("/api/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #TODO: If the user's credentials are correct, reroute them to the home page
        return f'{email}, {password}'

@app.route("/api/signup", methods=["POST", "GET"])
def sign_up():
    session["email"] = ""
    if request.method == "POST":
        valid = True
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        requirement_year = request.form.get("requirement-year")
        graduation_year = request.form.get("graduation-year")

        #Check to see that the user gives a valid gcc email address
        if email is None or email == "":
            valid = False
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            domain = re.search("@[\w.]+", email)
            if domain.group() == '@gcc.edu':
                print('valid')
            else:
                print('invalid')
        else:
            print("invalid")
        
        #Check to see whether or not the user gave a valid username
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if(string_check.search(username) != None):
            print("Special characters found")
        
        if username is None or username == "":
            print("username cannot be empty")

        #Check to see if the user gave a valid password
        password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)")
        if(password_regex.search(password)) != None:
            if(string_check.search(password) != None):
                print("Password has all needed characteristics")
        
        if valid:
            session["email"] = email
        
        print(session["email"])
                
        return f'{email} - {username} - {password} - {confirm_password} - {requirement_year} - {graduation_year}'

    if request.method == "GET":
        if session["email"]:
            return {
                "successful_account_creation": "true"
            }
        else:
            return {
                "successful_account_creation": "false"
            }