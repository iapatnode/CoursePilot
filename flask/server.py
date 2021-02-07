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
        # conn = connection()
        cursor = conn.cursor()
        cursor.execute("select * from Student")
        cursor.fetchall()
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
                degreeId int not null auto_increment,
                degreeName varchar(100),
                totalHours int,
                reqYear year,
                isMinor boolean,
                constraint pk_major_minor primary key (degreeId))""")

            cursor.execute("""create table if not exists StudentMajorMinor(
                email varchar(50),
                degreeId int,
                constraint pk_student_degree primary key (email, degreeId),
                constraint fk_student_info foreign key (email) references Student(email),
                constraint fk_degree_info foreign key (degreeId) references MajorMinor(degreeId))""")
            
            cursor.execute("""create table if not exists Course(
                courseCode varchar(12),
                courseName varchar(50),
                creditHours int,
                semester varchar(30),
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

            #Inserts some majors into database
            cursor.execute('''Insert into MajorMinor (degreeName, totalHours, reqYear, isMinor) values
                ("Communication Studies", 36, 2017, false),
                ("Accounting & Finance", 88, 2017, false),
                ("Philosophy", 30, 2017, false),
                ("Mechanical Engineering", 100, 2017, false),
                ("Music", 44, 2017, false),
                ("Undeclared", 0, 2017, false),

                ("Communication Studies", 36, 2018, false),
                ("Accounting & Finance", 88, 2018, false),
                ("Philosophy", 33, 2018, false),
                ("Mechanical Engineering", 100, 2018, false),
                ("Music", 44, 2018, false),
                ("Undeclared", 0, 2018, false),

                ("Communication Studies", 36, 2019, false),
                ("Accounting & Finance", 88, 2019, false),
                ("Philosophy", 33, 2019, false),
                ("Mechanical Engineering", 100, 2019, false),
                ("Music", 46, 2019, false),
                ("Undeclared", 0, 2019, false),

                ("Communication Arts", 36, 2020, false),
                ("Accounting & Finance", 88, 2020, false),
                ("Philosophy", 33, 2020, false),
                ("Mechanical Engineering", 100, 2020, false),
                ("Music", 46, 2020, false),
                ("Undeclared", 0, 2020, false)''')
            
            #Inserts some minors into database
            cursor.execute('''Insert into MajorMinor (degreeName, totalHours, reqYear, isMinor) values
                ("Astronomy", 21, 2017, true),
                ("Data Science", 19, 2017, true),
                ("French", 18, 2017, true),
                ("Nutrition", 15, 2017, true),
                ("Robotics", 20, 2017, true),
                ("Theatre", 24, 2017, true),

                ("Astronomy", 21, 2018, true),
                ("Data Science", 19, 2018, true),
                ("French", 18, 2018, true),
                ("Nutrition", 15, 2018, true),
                ("Robotics", 20, 2018, true),
                ("Theatre", 24, 2018, true),

                ("Astronomy", 21, 2019, true),
                ("Data Science", 19, 2019, true),
                ("French", 18, 2019, true),
                ("Nutrition", 15, 2019, true),
                ("Robotics", 20, 2019, true),
                ("Theatre", 24, 2019, true),

                ("Astronomy", 21, 2020, true),
                ("AI & Data Science", 22, 2020, true),
                ("French", 18, 2020, true),
                ("Nutrition", 15, 2020, true),
                ("Robotics", 20, 2020, true),
                ("Theatre", 24, 2020, true)''')

            #Inserts some courses into database
            cursor.execute('''Insert into Course(courseCode, courseName, creditHours, semester) values
                ("ACCT 201", "Principles of Accounting I", 3, "fall"),
                ("ART 208", "Pueblo Pottery", 3, "fall"),
                ("BIOL 101", "General Biology I", 4, "fall"),
                ("CHEM 111", "General Chemistry I", 3, "fall"),
                ("COMP 448", "Computer Security", 3, "fall"),
                ("MATH 331", "Theory Statistics 1", 3, "fall"),

                ("COMP 141", "Computer Programming I", 3, "both"),
                ("ENGR 156", "Intro to Engineering", 2, "both"),
                ("ENGR 301", "Ethics in Engineering & Robotics", 1, "both"),
                ("HUMA 102", "Civ/Biblical Revelation", 3, "both"),
                ("HUMA 301", "Civ/The Arts", 3, "both"),
                ("MATH 161", "Calculus I", 4, "both"),
                ("MATH 162", "Calculus II", 4, "both"),
                ("MUSI 119", "Grove City College Singers", 0, "both"),
                ("POLS 101", "Foundations of Political Science", 3, "both"),
                ("SOCI 251", "Courtship & Marriage", 3, "both"),

                ("ACCT 202", "Principles of Accounting II", 3, "spring"),
                ("BIOL 102", "General Biology II", 4, "spring"),
                ("CHEM 112", "General Chemistry II", 3, "spring"),
                ("COMP 350", "Software Engineering", 3, "spring"),
                ("MATH 332", "Theory Statistics II", 3, "spring"),
                ("MATH 421", "Abstract Algebra", 3, "spring")''')
            
            conn.commit()

        except Error as error:
            print("database not found:" + str(error))
    
    #DBMS connection cleanup
    cursor.close()
    # conn.close()

#Creates Course Pilot database and fills it with tables and data when application is opened
create_db()
conn = connection()
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
        # username = request.form.get("username")
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

                for degree in major:
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


@app.route("/api/home", methods=["GET"])
def home():
    #TODO: Return user data retrieved from database tables as needed
    return {
        "name": "Foo", 
        "email": "foo@bar.com",
        "graduation_year": "2021"
    }
