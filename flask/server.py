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
# scriptdir = os.path.dirname(os.path.abspath(__file__))
# with open(os.path.join(scriptdir, "config.json")) as text:
#     config = json.load(text)

# #Connects to server and creates database
# def create_db():
#     try:
#         with connect(host=config.get('host'), user=config.get('username'), password=config.get('password')) as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute("create database if not exists course_pilot")  
#     except Error as error:
#         print(error)

# #Establishes connection to database
# def connection():
#     try:
#         with connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database="course_pilot") as conn:
#             return conn
#     except Error as error:
#         print(error)

# #Creating and initializing the database
# def init_db():
#     try:
#         conn = connection()
#         with conn.cursor() as cursor:
#             cursor.execute("select * from Student")

#     #what is the difference between Exception and Error?
#     except Exception as exception:
#         try:
#             with conn.cursor as cursor:
        
#                 cursor.execute("""create table if not exists Student(
#                     username varchar(100), 
#                     email varchar(50),
#                     fname varchar(50),
#                     lname varchar(50),
#                     password varchar(30),
#                     graduationYear year,
#                     constraint pk_student primary key (username, email))""")
                
#                 cursor.execute("""create table if not exists MajorOrMinor(
#                     id char(6),
#                     name varchar(100),
#                     totalHours int,
#                     requirementYear year,
#                     isMinor boolean,
#                     constraint pk_major_minor primary key (id))""")
                
#                 cursor.execute("""create table if not exists Requirements(
#                     id char(6),
#                     category varchar(50),
#                     reqId char(6),
#                     constraint pk_requirements primary key (id),
#                     constraint fk_requirements_id foreign key (reqId) references Requirements(id))""")
                
#                 cursor.execute("""create table if not exists Course(
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     creditHours int,
#                     constraint pk_course primary key (courseCode, courseName))""")

#                 cursor.execute("""create table if not exists Class(
#                     section char,
#                     startTime time,
#                     endTime time,
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     constraint pk_class primary key (section, courseCode, courseName),
#                     constraint fk_class_course foreign key (courseCode, courseName) references Course(courseCode, courseName))""")
                
#                 #TODO: need to check this relationship
#                 cursor.execute("""create table if not exists Schedule(
#                     name varchar(50),
#                     dateModified date,
#                     username varchar(100),
#                     email varchar(50),
#                     constraint pk_schedule primary key (name, username, email),
#                     constraint fk_schedule_user foreign key (username, email) references Student(username, email))""")
                
#                 cursor.execute("""create table if not exists ClassDay(
#                     dayOfWeek varchar(50),
#                     classSection char,
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     constraint pk_class_day primary key (dayOfWeek, classSection, courseCode, courseName),
#                     constraint fk_class_details foreign key (classSection, courseCode, courseName) references Class(section, courseCode, courseName))""")
        
#                 cursor.execute("""create table if not exists ClassSchedule(
#                     scheduleName varchar(50),
#                     username varchar(100),
#                     email varchar(50),
#                     classSection char,
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     constraint pk_class_schedule primary key (scheduleName, username, email, classSection, courseCode, courseName),
#                     constraint fk_schedule_info foreign key (scheduleName, username, email) references Schedule(name, username, email),
#                     constraint fk_schedule_course_info foreign key (classSection, courseCode, courseName) references Class(section, courseCode, courseName))""")

#                 cursor.execute("""create table if not exists StudentCourse(
#                     hasTaken boolean,
#                     username varchar(100),
#                     email varchar(50),
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     constraint pk_student_course primary key (username, email, courseCode, courseName),
#                     constraint fk_course_info foreign key (courseCode, courseName) references Course(courseCode, courseName),
#                     constraint fk_student_info foreign key (username, email) references Student(username, email))""")

#                 cursor.execute("""create table if not exists CourseRequirements(
#                     courseCode varchar(12),
#                     courseName varchar(50),
#                     reqID char(6),
#                     constraint pk_course_requirements primary key (courseCode, courseName, reqID),
#                     constraint fk_requirements_id foreign key (reqID) references Requirements(id),
#                     constraint fk_requirements_course foreign key (courseCode, courseName) references Course(courseCode, courseName)""")
                
#                 cursor.execute("""create table if not exists MajorOrMinorRequirements(
#                     degreeID char(6),
#                     reqID char(6),
#                     constraint pk_major_minor_reqs primary key (degreeID, reqID),
#                     constraint fk_major_minor_id foreign key (degreeID) references MajorOrMinor(id),
#                     constraint fk_major_minor_req_id foreign key (reqID) references Requirements(id))""")
                
#                 cursor.execute("""create table if not exists StudentMajorOrMinor(
#                     username varchar(100),
#                     email varchar(50),
#                     degreeID char(6),
#                     constraint pk_student_major_or_minor primary key (username, email, degreeID),
#                     constraint fk_student_info foreign key (username, email) references Student(username, email),
#                     constraint fk_student_req_id foreign key (degreeID) references MajorOrMinor(id))""")
                
#                 #TODO: fill tables with dummy data

#         except Exception as exception:
#             print("database not found")
#             print(exception)

#Creates Course Pilot database and fills it with tables and data when application is opened
#create_db()
#init_db()


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
            session["email"] = email #use this to determine in the future who is logged in
            return redirect("http://localhost:3000/home")
        else:
            return redirect("http://localhost:3000/SignUp")

    if request.method == "GET":
        if session["email"]:
            return {
                "successful_account_creation": "true"
            }
        else:
            return {
                "successful_account_creation": "false"
            }

@app.route("/api/home", methods=["GET"])
def home():
    return {
        "name": "Foo", 
        "email": "foo@bar.com",
        "graduation_year": "2021"
    }
