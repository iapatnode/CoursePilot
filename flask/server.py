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
scriptdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptdir, "config.json")) as text:
    config = json.load(text)

#Establishes connection to database
def connection():
    try:
        conn = connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database=config.get('database'))
        return conn
    except Error as error:
        print(error)

#Creates global variable that creates connection to database
conn = connection()

@app.route("/api/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        valid = True

        #Check to see that a valid email was entered
        if email is None or email == "":
            valid = False
        domain = re.search("@[\w.]+", email)
        if domain.group() != '@gcc.edu':
            valid = False
        
        #Check to see that a password was entered
        if password is None or password == "":
            valid = False
        
        #Checks if student's credentials are in the database
        if valid:
            # conn = connection()
            cursor = conn.cursor(buffered=True)
            studentQuery = "select * from Student where email = %s and passwrd = %s"
            studentCredentials = (email, password)

            try:
                cursor.execute(studentQuery, studentCredentials)
                conn.commit()

                #Checks if user with credentials exists
                if cursor.rowcount == 0:
                    print("User not found")
                    valid = False
                
            except Error as error:
                print("Query did not work: " + str(error))
                valid = False
            
            #DBMS connection cleanup
            cursor.close()
        #     conn.close()

        if valid:
            session["email"] = email
            return redirect("http://localhost:3000/home")
        
        #If the user's credentials are not found, redirect them back to the login page
        else:
            return redirect("http://localhost:3000")

@app.route("/api/signup", methods=["POST", "GET"])
def sign_up():
    session["email"] = ""
    if request.method == "POST":
        valid = True
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        requirement_year = request.form.get("requirement-year")
        graduation_year = request.form.get("graduation-year")
        major = request.form.getlist("major")
        minor = request.form.getlist("minor")
        print(f'{email}, {password}, {confirm_password}, {requirement_year}, {graduation_year}, {major}, {minor}')

        #Check to see that the user gives a valid gcc email address
        if email is None or email == "":
            valid = False
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            domain = re.search("@[\w.]+", email)
            if domain.group() == '@gcc.edu':
                print("valid")
            else:
                valid = False
        else:
            valid = False
        
        # #Check to see whether or not the user gave a valid username
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        #Check to see if the user gave a valid password
        password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)")
        if(password_regex.search(password)) != None:
            if(string_check.search(password) != None):
                print("Password has all needed characteristics")
            else:
                valid = False
        
        #Check to see if the two password fields match
        if password != confirm_password:
            valid = False

        #Check to see that the user's major/minor selections are valid
        if major is None or major == "":
            valid = False

        print(major)
        
        if minor is None or minor == "":
            valid = False
        
        print(minor)
        if valid:
            # conn = connection()
            cursor = conn.cursor()
            newStudentQuery = "Insert into Student values (%s, %s, %s)"
            newStudentData = (email, password, graduation_year)

            studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"

            #TODO: add student major/minor information

            #adds student and his/her info to the database
            try:
                cursor.execute(newStudentQuery, newStudentData)

                conn.commit()
            except error as error:
                #If you cannot insert the invidual into the database, print error and reroute
                print("Insertion in database unsuccessful: " + str(error))
                return redirect("http//localhost:3000/SignUp")
            
            #DBMS connection cleanup
            cursor.close()
            # conn.close()

            session["email"] = email #use this to determine in the future who is logged in
            return redirect("http://localhost:3000/home")
        else:
            return redirect("http://localhost:3000/SignUp")

    if request.method == "GET":
        
        #TODO: Replace these lists with accurate lists containing all majors and minors
        return {
            "majors": [
                "computer science", 
                "mechanical engineering", 
                "accounting"
            ],
            "minors": [
                "none",
                "computer science", 
                "finance", 
                "biblical and religious studies",
                "data science"
            ]
        }

@app.route("/api/home", methods=["GET", "POST"])
def home():
    #TODO: Return user data retrieved from database tables as needed
    if request.method == "GET":
        return {
            "name": "Foo", 
            "email": "foo@bar.com",
            "graduation_year": "2021"
        }
    if request.method == "POST":
        return redirect("http://localhost:3000/Schedule")

# @app.route("/api/search", method=["POST"])
# def autoSearch():
#     if request.method == "POST":
#         cursor = conn.cursor()
#         conn.commit()
#         return redirect("http://localhost:3000/Profile")