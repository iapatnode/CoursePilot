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

"""
----- Login Page API Endpoint -----

Purpose: Define server-side logic to run when a user sends
         either a get or post request from the login page
"""
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
        
        # If student is in database, provided valid username password combination
        if valid:
            session["email"] = email #Used to identify which user is logged in
            return redirect("http://localhost:3000/home") #Redirect user to the home page
        
        #If the user's credentials are not found, redirect them back to the login page
        else:
            return redirect("http://localhost:3000")


"""
----- Sign-In Page API Endpoint -----

Function: Handle requests sent to the server by 
          the user from the sign-up page
"""
@app.route("/api/signup", methods=["POST", "GET"])
def sign_up():

    session["email"] = "" #Reset session email so a user is now shown as logged in

    # If the user sends a post request, get information and add it to database if valid
    if request.method == "POST":
        valid = True
        # Get all user data
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        email = json_data.get("email")
        password = json_data.get("password")
        confirm_password = json_data.get("confirm_password")
        requirement_year = json_data.get("requirement_year")
        graduation_year = json_data.get("graduation_year")
        major = json_data.get("major")
        print(major)
        minor = json_data.get("minor")
        print(minor)

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

        #Check to see if the user gave a valid password
        special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)")

        #Check if passwords has mix of uppercase, lowercase, and numbers
        if(password_regex.search(password)) == None:
            valid = False

        #Check if password has special characters    
        if(special_characters.search(password) == None):
            valid = False
        
        #Check to see if the two password fields match
        if password != confirm_password:
            valid = False

        #Check to see that the user's major/minor selections are valid
        if major is None or major == "":
            valid = False

        #If all information from form data is valid, add to database
        if valid:
            #Establish db cursor and define queries/parameters
            cursor = conn.cursor()
            newStudentQuery = "Insert into Student values (%s, %s, %s)"
            newStudentData = (email, password, graduation_year)

            #adds student and his/her info to the database
            try:
                cursor.execute(newStudentQuery, newStudentData)
                print("Inserted student into the database")
                conn.commit()

            except error as error:
                #If you cannot insert the invidual into the database, print error and reroute
                print("Insertion in database unsuccessful: " + str(err))
                return redirect("http//localhost:3000/SignUp")
            
            #Adds student major information to database
            try:
                studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"

                #For every major that a student chooses, add it to the StudentMajorMinor database table
                for m in major:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (m, requirement_year, 0))
                    result = cursor.fetchall()

                    #Get the major id of the major currently being added to the database
                    for row in result:
                        mid = row[0]
                    
                    #Add the current major to the database
                        addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                        cursor.execute(addToMajorMinor, (email, mid))
                        print("Added a major")
                
                conn.commit()
                
                #For every minor that the student chooses, add it to the StudentMajorMinor database table
                if minor is not None or minor != "":
                    for mm in minor:
                        mid = 0
                        cursor.execute(studentDegreeQuery, (mm, requirement_year, 1))
                        result = cursor.fetchall()

                        #Get the minor if of the minor to be added to the database
                        for row in result:
                            mid = row[0]
                        
                        #Add the current minor to the database
                            addToMinor = "insert into StudentMajorMinor values (%s, %s)"
                            cursor.execute(addToMinor, (email, mid))
                            print("Added a minor")
                    
                    conn.commit()
            
            except error as error:
                #If you cannot insert the major/minor into the database, print error and reroute
                print("Insertion in database unsuccessful: " + str(err))
                return redirect("http//localhost:3000/SignUp")

            #DBMS connection cleanup
            cursor.close()

            session["email"] = email #use this to determine in the future who is logged in

            return jsonify({'redirect_to_home': True}), 200 #Response sent to client to indicate success
        else:
            return jsonify({'redirect_to_home': False}), 400 #Response sent to client to indicate failure

    #If the user sends a get request, return a list of all majors and minors to be displayed in dropdown menus
    if request.method == "GET":
        # Get a list of all majors and minors from the database, append them to all_majors, list of  dictionaries
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

        #Return list of all majors and minors in the database
        return {
            "majors": all_majors,
            "minors": all_minors
        }

"""
----- Home Page API Endpoint -----

Function: Handle requests sent by the user from the home page
          of course pilot
"""
@app.route("/api/home", methods=["GET", "POST"])
def home():
    #If a get request is sent, return all schedule information for the user who is currently logged in
    if request.method == "GET":
        email = session["email"]
        all_schedules = []
        cursor = conn.cursor()
        get_schedules_query = "select * from Schedule where email = %s"
        cursor.execute(get_schedules_query, (email,))
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
        #print(all_schedules)
        return json.dumps(all_schedules)

    #If a post request is sent, add schedule information to the Schedule database
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
        # class_query = "select * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like ?;", (f"%{(search_val)}%",)
        
        # print(search_val)
        # cursor.execute(class_query)

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
        ''', (f"%{(search_val)}%",))

        class_table = cursor.fetchall()
        # print(class_table)

        result_string = ""
        for row in class_table:
            classArray.append(row[0])
            classArray.append(row[2])
            for item in row:
                # print(row)
                result_string += str(item) + "\n"

        for row in classArray:
            print(row)
            
        
        return result_string
        # return (search_val)

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


# @app.route("/api/schedule/<name>")
# def schedule_with_name(name):
#     cursor = conn.cursor()
#     email = session["email"]
#     schedule_course_list = []
#     if request.method == "GET":
#         schedule_course_info = """
#             select * from Class join ScheduleClass on Class.courseCode = ScheduleClass.courseCode
#             where schedule_name = %s and email = %s
#             """
#         cursor.execute(schedule_course_into, (name, email))
#         results = cursor.fetchall()
#         for course in results:
#             section = course[0]
#             start_time = course[2]
#             end_time = course[3]
#             meeting_days = course[4]
#             course_code = course[5]
#             schedule_course_list.extend(
#                 {
#                     "code": course_code,
#                     "section": section,
#                     "start": start_time,
#                     "end": end_time,
#                     "days": meeting_days
#                 }
#             )
#         #Now, need to create a new calendar entry for each day a class is offered
#         data = []
#         i = 1
#         for c in schedule_course_list:
#             for day in c["days"]:
#                 schedule_event = {}
#                 if day == "M":
#                     schedule_event = {
#                         "id": i,
#                         "text": f"{c["code"]} {c["section"]}",
#                         "start": f"2013-03-25T{c["start"]}",
#                         "end": f"2013-03-25T{c["end"]}",
#                         "resource": "monday"
#                     }
#                 elif day == "T":
#                     schedule_event = {
#                         "id": i,
#                         "text": f"{c["code"]} {c["section"]}",
#                         "start": f"2013-03-25T{c["start"]}",
#                         "end": f"2013-03-25T{c["end"]}",
#                         "resource": "tuesday"
#                     }
#                 elif day == "W":
#                     schedule_event = {
#                         "id": i,
#                         "text": f"{c["code"]} {c["section"]}",
#                         "start": f"2013-03-25T{c["start"]}",
#                         "end": f"2013-03-25T{c["end"]}",
#                         "resource": "wednesday"
#                     }
#                 elif day == "R":
#                     schedule_event = {
#                         "id": i,
#                         "text": f"{c["code"]} {c["section"]}",
#                         "start": f"2013-03-25T{c["start"]}",
#                         "end": f"2013-03-25T{c["end"]}",
#                         "resource": "thursday"
#                     }
#                 else:
#                     schedule_event = {
#                         "id": i,
#                         "text": f"{c["code"]} {c["section"]}",
#                         "start": f"2013-03-25T{c["start"]}",
#                         "end": f"2013-03-25T{c["end"]}",
#                         "resource": "friday"
#                     }
#                 i = i + 1
#             data.append(schedule_event)
            
#         return json.dumps(data)


# function to auto generate the schedule
#def AutoGenerateSchedule():
#    print("testing!")

    # this will be the list that is the final recommended schedule
#    recommendedSchedule = []
    # This will be a list of the classes 
#    takenCourses = getTakenCourses()

#    majorCourses = []

#    for majorCourse in majorCourses:
#        for takenCourse in takenCourses:
            # need to add if student has not taken prereqs
            # need to add if the class is not offered in the semester selected
#            if (takenCourse != majorCourse):
#                recommendedSchedule.append(majorCourse)





def getTakenCourses():
    cursor = conn.cursor()
    try:
        cursor.execute("select courseCode from StudentCourses")

        takenCourses = cursor.fetchall()
        return takenCourses
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
