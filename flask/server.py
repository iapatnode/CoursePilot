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
        conn = connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database="course_pilot")
        return conn
    except Error as error:
        print(error)

#Creating and initializing the database
def init_db():
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select * from Student")
        #Why does it print here?
        # print("table not found")

    #what is the difference between Exception and Error?
    except Error as error:
        try:
            #MAY ADD REQYEAR AS A ELEMENT
            #creates all tables for database
            cursor.execute("""create table if not exists Student( 
                email varchar(50),
                passwrd varchar(30),
                gradYear year,
                constraint pk_student primary key (email))""")

            cursor.execute("""create table if not exists MajorMinor(
                degreeId char(6),
                degreeName varchar(100),
                totalHours int,
                reqYear year,
                isMinor boolean,
                constraint pk_major_minor primary key (degreeId))""")

            cursor.execute("""create table if not exists StudentMajorMinor(
                email varchar(50),
                degreeId char(6),
                constraint pk_student_degree primary key (email, degreeId),
                constraint fk_student_info foreign key (email) references Student(email),
                constraint fk_degree_info foreign key (degreeId) references MajorMinor(degreeId))""")
            
            cursor.execute("""create table if not exists Course(
                courseCode varchar(12),
                courseName varchar(50),
                creditHours int,
                constraint pk_course primary key (courseCode))""")

            cursor.execute("""create table if not exists StudentCourses(
                email varchar(50),
                courseCode varchar(12),
                constraint pk_student_courses primary key (email, courseCode),
                constraint fk_student_details foreign key (email) references Student(email),
                constraint fk_course_info foreign key (courseCode) references Course(courseCode))""")

            cursor.execute("""create table if not exists Class(
                section char,
                startTime time,
                endTime time,
                courseCode varchar(12),
                constraint pk_class primary key (section, courseCode),
                constraint fk_class_course foreign key (courseCode) references Course(courseCode))""")
            
            cursor.execute("""create table if not exists ClassDays(
                section char, 
                courseCode varchar(12),
                dayOfWeek varchar(30),
                constraint pk_class_days primary key (section, courseCode, dayOfWeek),
                constraint fk_class_info foreign key (section, courseCode) references Class(section, courseCode))""")
            
            cursor.execute("""create table if not exists Schedule(
                scheduleName varchar(50),
                dateModified date,
                email varchar(50),
                constraint pk_schedule primary key (scheduleName, email),
                constraint fk_schedule_user foreign key (email) references Student(email))""")
            
            cursor.execute("""create table if not exists ScheduleClass(
                scheduleName varchar(50),
                email varchar(50),
                classSection char,
                courseCode varchar(12),
                constraint pk_class_schedule primary key (scheduleName, email, classSection, courseCode),
                constraint fk_schedule_info foreign key (scheduleName, email) references Schedule(scheduleName, email),
                constraint fk_schedule_course_info foreign key (classSection, courseCode) references Class(section, courseCode))""")
            
            #TODO: need to create tables for Requirements and Prereqs
            conn.commit()

            #TODO: fill tables with dummy data

        except Error as error:
            print("database not found:" + str(error))
    
    #DBMS connection cleanup
    cursor.close()
    conn.close()

#Creates Course Pilot database and fills it with tables and data when application is opened
create_db()
init_db()


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
        
        if valid:
            conn = connection()
            cursor = conn.cursor()
            studentQuery = "select * from Student where email = %s and passwrd = %s"
            studentCredentials = (email, password)

            try:
                cursor.execute(studentQuery, studentCredentials)
                conn.commit()

                #Checks if user with credentials exists
                if cursor.fetchone() is None:
                    print("User not found")
                    valid = False
                
            except Error as error:
                print("Query did not work: " + str(error))
                valid = False
            
            #DBMS connection cleanup
            cursor.close()
            conn.close()

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
        # username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        requirement_year = request.form.get("requirement-year")
        graduation_year = request.form.get("graduation-year")
        major = request.form.get("major")
        minor = request.form.get("minor")

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
        # if(string_check.search(username) != None):
        #     valid = False
        
        # if username is None or username == "":
        #     valid = False

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
        
        if minor is None or minor == "":
            valid = False
        
        if valid:
            conn = connection()
            cursor = conn.cursor()
            newStudentQuery = "Insert into Student values (%s, %s, %s)"
            newStudentData = (email, password, graduation_year)

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
            conn.close()

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


@app.route("/api/home", methods=["GET"])
def home():
    #TODO: Return user data retrieved from database tables as needed
    return {
        "name": "Foo", 
        "email": "foo@bar.com",
        "graduation_year": "2021"
    }
