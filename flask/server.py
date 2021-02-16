from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os
import re, json
from mysql.connector import connect, Error
from datetime import datetime

#Flask App Setup
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
        else:
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
            # conn = connection()
            cursor = conn.cursor()
            newStudentQuery = "Insert into Student values (%s, %s, %s)"
            newStudentData = (email, password, graduation_year)
            session["email"] = email
            print(session["email"])

            #adds student and his/her info to the database
            try:
                cursor.execute(newStudentQuery, newStudentData)
                print("Inserted student into the database")

                conn.commit()
            except Error as error:
                #If you cannot insert the invidual into the database, print error and reroute
                print("Insertion in database unsuccessful: " + str(error))
                return redirect("http//localhost:3000/SignUp")
            
            #Adds student major information to database
            try:
                studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"
                for m in major:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (m, requirement_year, 0))
                    result = cursor.fetchall()
                    for row in result:
                        mid = row[0]
                    
                        addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                        cursor.execute(addToMajorMinor, (email, mid))
                        print("Inserted one major")
                        conn.commit()
                
                for mm in minor:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (mm, requirement_year, 1))
                    result = cursor.fetchall()
                    for row in result:
                        mid = row[0]
                    
                        addToMinor = "insert into StudentMajorMinor values (%s, %s)"
                        cursor.execute(addToMinor, (email, mid))
                        print("Inserted one minor")
                        conn.commit()

                print("Added majo/minorr to the database")
            
            except Error as error:
                #If you cannot insert the major/minor into the database, print error and reroute
                print("Insertion in database unsuccessful: " + str(error))
                return redirect("http//localhost:3000/SignUp")

            #DBMS connection cleanup
            cursor.close()
            # conn.close()

            session["email"] = email #use this to determine in the future who is logged in
            print("Made it here")
            # return redirect("http://localhost:3000/home")
            return jsonify({'redirect_to_home': True}), 200
        else:
            return jsonify({'redirect_to_home': False}), 400

    if request.method == "GET":
        print(session.get("email"))
        # Get a list of all majors and minors from the database
        cursor = conn.cursor()
        major_query = "select distinct degreeName from MajorMinor where isMinor = 0"
        cursor.execute(major_query)
        result = cursor.fetchall()
        all_majors = []
        for entry in result:
            all_majors.append(entry[0])
    
        minor_query = "select distinct degreeName from MajorMinor where isMinor = 1"
        cursor.execute(minor_query)
        result = cursor.fetchall()
        all_minors = []
        for entry in result:
            all_minors.append(entry[0])
        
        cursor.close()

        return {
            "majors": all_majors,
            "minors": all_minors
        }

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

#attempt at using AJAX to load data from search bar        
# @app.route("/search-auto/", methods=["POST"])
# def autoSearch():
#     cursor = conn.cursor()
#     search_val = request.form.get("outlined-search")
#     request_json = request.get_json()

#     search_item = request_json["outlined-search"]
#     print(search_val)
#     if search_item:
#         sets = cursor.execute(''' 
#             SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
#         ''', (f"%{(search_val)}%",))
    
#     else:
#         sets = []
    
#     return jsonify(sets), 200

@app.route("/api/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search_val = ""
        search_val = request.form.get("outlined-search")
        cursor = conn.cursor()
        classArray = []
        courseArray = []
        #request_json = request.get_json()
        print('here')
        # class_query = "select * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like ?;", (f"%{(search_val)}%",)
        
       # search_item = request_json["outlined-search"]
        #print("search Item:" + search_item)

        print(search_val)
        # cursor.execute(class_query)

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
        ''', (f"%{(search_val)}%",))

        # cursor.execute('''
        #     SELECT * from Course where Course.courseCode like %s;
        # ''', (f"%{(search_val)}%",))

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
                # print(row)
                result_string += str(item)

        for row in classArray:
            print(row)
            
        
        # return (result_string)
        # return (search_val)
        return json.dumps(courseArray)

@app.route('/api/schedule', methods=["GET", "POST"])
def schedule():
     if request.method == "GET":
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



# function to auto generate the schedule
#def AutoGenerateSchedule():
#    print("testing!")


#    recommendedSchedule = []

#    takenCourses = getTakenCourses()

#    majorCourses = []

#    for majorCourse in majorCourses:
#        for takenCourse in takenCourses:
#            # need to add if student has not taken prereqs
#            # need to add if the class is not offered in the semester selected
#            if (takenCourse != majorCourse):
#                recommendedSchedule.append(majorCourse)





#def getTakenCourses():
#    takenCourses = []
#    return takenCourses

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
