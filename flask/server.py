from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os, re, json
from datetime import datetime
from mysql.connector import connect, Error

import dbQueries as db_queries
import degreeReport as degree_report

#Flask App Setup
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.urandom(32)

#Settings for testing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Credentials for database connection
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
        else:
            domain = re.search("@[\w.]+", email)
            if domain.group() != '@gcc.edu':
                valid = False
        
        #Check to see that a password was entered
        if password is None or password == "":
            valid = False
        
        #Checks if student's credentials are in the database
        if valid:
            valid = db_queries.validLogin(email, password)

        if valid:
            db_queries.validLogin(email, password)
        
            session["email"] = email
            return redirect("http://localhost:3000/home")
        
        #If the user's credentials are not found, redirect them back to the login page
        else:
            return redirect("http://localhost:3000")

@app.route("/api/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        valid = True
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        email = json_data.get("email")
        password = json_data.get("password")
        confirm_password = json_data.get("confirm_password")
        requirement_year = json_data.get("requirement_year")
        graduation_year = json_data.get("graduation_year")
        major = json_data.get("major")
        minor = json_data.get("minor")
        print(f'{email}, {password}, {confirm_password}, {requirement_year}, {graduation_year}, {major}, {minor}')

        #Check to see that the user gives a valid gcc email address
        if email is None or email == "":
            print("email is wrong")
            valid = False
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            domain = re.search("@[\w.]+", email)
            if domain.group() != '@gcc.edu':
                print("email is wrong (non-gcc)")
                valid = False
        
        # #Check to see whether or not the user gave a valid username
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        #Check to see if the user gave a valid password
        password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)")
        if(password_regex.search(password)) == None:
            print("Password has no uppercase or decimal or lowercase")
            valid = False
            
        if(string_check.search(password) == None):
            print("Password has no special characters")
            valid = False
        
        #Check to see if the two password fields match
        if password != confirm_password:
            print("Passwords do not match")
            valid = False

        #Check to see that the user's major/minor selections are valid
        if major is None or major == "":
            print("Need to enter a major")
            valid = False

        print(major)
        print(valid)

        if valid:
            db_queries.validPostSignUp(email, password, graduation_year, requirement_year, major, minor)

            if valid:
                session["email"] = email #use this to determine in the future who is logged in
                print(session["email"])
                print("Made it here")
                return jsonify({'redirect_to_home': True}), 200
            else:
                return redirect("http//localhost:3000/SignUp")
        else:
            return jsonify({'redirect_to_home': False}), 400

    if request.method == "GET":
        print(session.get("email"))
        return db_queries.validGetSignUp()

@app.route("/api/home", methods=["GET", "POST"])
def home():
    #TODO: Return user data retrieved from database tables as needed
    if request.method == "GET":
        all_schedules = []
        cursor = conn.cursor()
        get_schedules_query = """ SELECT * FROM Schedule WHERE email = "dybasjt17@gcc.edu" """
        cursor.execute(get_schedules_query)
        result = cursor.fetchall()
        for schedule in result:
            all_schedules.append(
                {
                    "scheduleName": schedule[0],
                    "dateModified": str(schedule[1]),
                    "email": schedule[2],
                    "scheduleSemester": schedule[3]
                }
            )
        print(all_schedules)
        return json.dumps(all_schedules)

    if request.method == "POST":
        cursor = conn.cursor()

        schedule_name = request.form.get("schedule-name")
        schedule_semester = request.form.get("schedule-semester")
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

        insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
        cursor.execute(insert_schedule_query, (schedule_name, formatted_date, session["email"], schedule_semester))
        conn.commit()

        return redirect("http://localhost:3000/Schedule")

@app.route("/api/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search_val = ""
        search_val = request.form.get("outlined-search")
        cursor = conn.cursor()
        classArray = []
        courseArray = []

        print(search_val)

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
        ''', (f"%{(search_val)}%",))

        class_table = cursor.fetchall()
        print(class_table)

        result_string = ""
        for row in class_table:
            course_dict = {
                "course_code": row[0],
                "course_semester": row[1],
                "course_name": row[2],
                "course_credits": row[3],
                "course_section": row[4],
                "course_time": str(row[6])
            }
            courseArray.append(course_dict)

            for item in row:
                result_string += str(item)

        for row in classArray:
            print(row)


        return json.dumps(courseArray)

@app.route('/api/schedule', methods=["GET", "POST"])
def schedule():
     if request.method == "GET":
        cursor = conn.cursor()
        classArray = []
        courseArray = []

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode order by Course.courseCode;
        ''',)

        class_table = cursor.fetchall()

        result_string = ""
        for row in class_table:
            course_dict = {
                "course_code": row[0],
                "course_semester": row[1],
                "course_name": row[2],
                "course_credits": row[3],
                "course_section": row[4],
                "course_time": str(row[6])
            }
            courseArray.append(course_dict)

            for item in row:
                result_string += str(item)

        for row in classArray:
            print(row)
            
        return json.dumps(courseArray)

@app.route("/api/filledSchedule", methods=["GET"])
def get_filled_schedule():
    data = json.dumps(
        [           
            {
            "id": 1,
            "text": "SOCI 101",
            "start": "2013-03-25T12:00:00",
            "end": "2013-03-25T14:00:00",
            "resource": "monday"
            },
            {
            "id": 2,
            "text": "COMP 141",
            "start": "2013-03-25T15:00:00",
            "end": "2013-03-25T17:00:00",
            "resource": "wednesday"
            },
            {
            "id": 3,
            "text": "Event 3",
            "start": "2013-03-25T18:00:00",
            "end": "2013-03-25T19:00:00",
            "resource": "friday"
            },
        ]
    )

    return data


@app.route("/api/degreereport", methods=["GET", "POST"])
def report():

    if request.method == "GET":
        #TODO: FIX WHEN THEY FIX SESSION  
        degreeIds = degree_report.getStudentMajors(session['email'])
        
        studentDegreeReqs = degree_report.getMajorRequirements(degreeIds[0][0])

        #TODO: GET CLASSES THAT THEY HAVE ALREADY TAKEN
        #format stays the same
        return json.dumps(studentDegreeReqs)
    else:
        return "POST FUCKED!"


def getClasses():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Class")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))
    
def getCourse():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Course")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getMajorMinor():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from MajorMinor")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getMajorMinorRequirements():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from MajorMinorRequirements")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getPrerequisite():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Prerequisite")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getReqCourses():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from ReqCourses")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getRequirement():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Requirement")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getSchedule():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Schedule")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getScheduleClass():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from ScheduleClass")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getStudent():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from Student")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getStudentCourses():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from StudentCourses")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))

def getStudentMajorMinor():
    cursor = conn.cursor()
    try:
        cursor.execute("select * from StudentMajorMinor")

        info = cursor.fetchall()
        print(info)
    except error as error:
        print("Could not pull the data" + str(error))
