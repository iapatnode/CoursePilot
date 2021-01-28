from flask import Flask, request, render_template, redirect, session, Response
import os
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

#Settings for testing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    #TODO: If the user's email and password are correct, route them to the home page
    return f'{email}, {password}'

@app.route("/SignUp/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        requirement_year = request.form.get("requirement-year")
        graduation_year = request.form.get("graduation-year")
        return f'{email} - {username} - {password} - {confirm_password} - {requirement_year} - {graduation_year}'