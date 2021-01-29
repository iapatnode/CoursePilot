from flask import Flask, request, render_template, redirect, session, Response
from flask_cors import CORS
import os
import re


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.urandom(32)

#Settings for testing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #TODO: If the user's credentials are correct, reroute them to the home page
        return f'{email}, {password}'

@app.route("/SignUp/", methods=["POST", "GET"])
def sign_up():
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
                

        return f'{email} - {username} - {password} - {confirm_password} - {requirement_year} - {graduation_year}'
    else:
        return 'Test'


@app.route("/Test/", methods=["GET"])
def test():
    return f'This is the test page'