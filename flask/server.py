from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route("/", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return f'{email}, {password}'

@app.route("/SignUp/", methods=["POST"])
def sign_up():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    requirement_year = request.form.get("requirement-year")
    graduation_year = request.form.get("graduation-year")
    return f'{email}, {username}, {password}, {confirm_password}, {requirement_year}, {graduation_year}'
