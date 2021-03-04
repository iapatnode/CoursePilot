from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os, re, json
from datetime import datetime
from mysql.connector import connect, Error

import dbQueries as db_queries
import degreeReport as report

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

#User Email Variable
user_email = ""

#Semester Selection Variable
semester_selection = ""

#Get schedule name
schedule_name = ""

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
            global user_email
            user_email = email
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

            global user_email
            user_email = email
            print("Made it here")
            # return redirect("http://localhost:3000/home")
            return jsonify({'redirect_to_home': True}), 200
        else:
            return jsonify({'redirect_to_home': False}), 400

    if request.method == "GET":
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
    global user_email
    global semester_selection
    if request.method == "GET":
        # email = session.get("email")
        # print(email)
        all_schedules = []
        cursor = conn.cursor()
        print(f"email: {user_email}")
        get_schedules_query = ('''
            SELECT * FROM Schedule WHERE email = %s;
            ''')
        cursor.execute(get_schedules_query, (user_email,))
        result = cursor.fetchall()
        for schedule in result:
            # print(schedule)
            all_schedules.append(
                {
                    "scheduleName": schedule[0],
                    "dateModified": str(schedule[1]),
                    "email": schedule[2],
                    "scheduleSemester": schedule[3]
                }
            )
        # print(all_schedules)
        return json.dumps(all_schedules)

    if request.method == "POST":
        cursor = conn.cursor()
        global schedule_name
        schedule_name = request.form.get("schedule-name")
        schedule_semester = request.form.get("schedule-semester")
        semester_selection = request.form.get("schedule-semester")
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')
        session["schedule_semester"] = schedule_semester #Test to load courses and whatnot
        print(f"{schedule_name} {formatted_date} {user_email} {schedule_semester}")

        insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
        cursor.execute(insert_schedule_query, (schedule_name, formatted_date, user_email, schedule_semester))
        conn.commit()

        schedule_url = "http://localhost:3000/Schedule"

        url = '{}?{}'.format(schedule_url, schedule_name)

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
            print(row)
            course_dict = {
                "course_code": row[0],
                "course_semester": row[1],
                "course_name": row[2],
                "course_credits": row[3],
                "course_section": row[4],
                "course_time": str(row[6]),
                "course_end": str(row[7]),
            }
            courseArray.append(course_dict)

            for item in row:
                result_string += str(item)

        for row in classArray:
            print(row)


        return json.dumps(courseArray)

@app.route('/api/schedule', methods=["GET", "POST"])
def schedule():
    global schedule_name
    global user_email
    if request.method == "GET":
        print("Method is get")
        print(user_email)
        cursor = conn.cursor()
        classArray = []
        courseArray = []
        

        cursor.execute('''
            SELECT scheduleSemester from Schedule WHERE scheduleName like %s AND email like %s;
            ''', (f"%{(schedule_name)}%", f"%{(user_email)}%",))

        semester = cursor.fetchall()
        semester_current = ""
        for result in semester:
            semester_current = result[0]

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode WHERE courseSemester like %s order by Course.courseCode;
            ''', (f"%{(semester_current)}%",))

        class_table = cursor.fetchall()

        result_string = ""
        for row in class_table:
            course_dict = {
                "course_code": row[0],
                "course_semester": row[1],
                "course_name": row[2],
                "course_credits": row[3],
                "course_section": row[4],
                "course_time": str(row[6]),
                "course_end": str(row[7]),
                "days": row[8]
            }
            courseArray.append(course_dict)

            for item in row:
                result_string += str(item)

        for row in classArray:
            print(row)
        return json.dumps(courseArray)
    
    if request.method == "POST":
        # global schedule_name
        # global user_email
        # global semester_selection
        print("method is post")
        print(user_email)
        cursor = conn.cursor()
        data = request.data.decode("utf-8")
        # print("data: ")
        # print(data)
        json_data = json.loads(data)
        code_pt_1 = ""
        code_pt_2 = ""
        section = ""
        codes = []
        sections = []
        classes = []

        #Get the appropriate semester from the Schedule table
        cursor.execute('''
            SELECT scheduleSemester from Schedule WHERE scheduleName like %s AND email like %s;
            ''', (f"%{(schedule_name)}%", f"%{(user_email)}%",))

        semester = cursor.fetchall()
        for result in semester:
            semester_current = result[0]

        #Do some formatting with the strings
        for course in json_data.get("courses"):
            course_string = course.replace(" ", "-")
            # print(course_string)
            index = course_string.index('-')
            # print(index)
            code_pt_1 = course_string[0: index + 4]
            # print(code_pt_1)
            sec_ind = len(course_string) - 1
            # print(sec_ind)
            section = course_string[sec_ind]
            # print(section)
            code = code_pt_1.replace("-", " ")
            # print(code)
            course_w_section = f"{code} {section}"
            codes.append(code)
            sections.append(section)

            #Get class info from Class table using code and section as keys
            cursor.execute(''' 
                SELECT * from Class WHERE courseCode like %s AND courseSection like %s;
                ''', (f"%{(code)}%", f"%{(section)}",))

            schedule_class = cursor.fetchall()
            print(schedule_class[0])
            classes.append(schedule_class[0])

        # Insert in to ScheduleClass query
        classInsert = "INSERT into ScheduleClass (scheduleName, email, courseSection, courseCode, meetingDays, classSemester) VALUES (%s, %s, %s, %s, %s, %s)"

        #TODO: Iterate over all of the codes and sections, add them to the database
        # Loop that assigns all neccesary items for a class to an array
        for result in classes:
            schedule_items = [schedule_name, user_email, result[0], result[5], result[4], result[1]]
            print(schedule_items)


            cursor.execute(classInsert, (schedule_name, user_email, result[0], result[5], result[4], result[1]))
        conn.commit()
        # print(f"{codes}{sections}")
        return f"{codes} {sections}"


@app.route("/api/getScheduleInfo", methods=["GET"])
def get_new_schedule():
    if request.method == "GET":
        global schedule_name
        global user_email
        global semester_selection
        if schedule_name != "":
            query = "select * from ScheduleClass where scheduleName = %s and email = %s"
            cursor = conn.cursor()
            cursor.execute(query, (schedule_name, user_email,))
            course_code_list = []
            course_section_list = []
            course_meeting_days = []
            course_start_times = []
            course_end_times = []
            course_name_list = []
            start_string = []
            end_string = []
            return_list = []
            semester = ""
            result = cursor.fetchall()
            for row in result:
                course_code_list.append(row[3])
                course_section_list.append(row[2])
                course_meeting_days.append(row[4])
                semester = row[5]
            course_info_query = "select startTime, endTime from Class where courseSection = %s and courseCode = %s and classSemester = %s"
            for i in range(len(course_code_list)):
                cursor.execute(course_info_query, (course_section_list[i], course_code_list[i], semester))
                result = cursor.fetchall()
                for row in result:
                    course_start_times.append(row[0])
                    course_end_times.append(row[1])
            i = 0
            course_name_query = "select courseName from Course where courseSemester = %s and courseCode = %s"
            for code in course_code_list:
                cursor.execute(course_name_query, (semester, code,))
                result = cursor.fetchall()
                for row in result:
                    course_name_list.append(row[0])
            print(course_name_list)
            for time in course_start_times:
                if len(str(time)) < 8:
                    time = f"0{str(time)}"
            for time in course_end_times:
                if len(str(time)) < 8:
                    time = f"0{str(time)}"
            for entry in course_meeting_days:
                for day in entry:
                    resource = ""
                    if day == 'M':
                        resource = "monday"
                    if day == 'T':
                        resource = "tuesday"
                    if day == 'W':
                        resource = "wednesday"
                    if day == 'R':
                        resource = "thursday"
                    if day == 'F':
                        resource = "friday"
                    start_time = ""
                    end_time = ""
                    if len(str(course_start_times[i])) < 8:
                        start_time = f"0{course_start_times[i]}"
                    else:
                        start_time = course_start_times[i]
                    if len(str(course_end_times[i])) < 8:
                        end_time = f"0{course_end_times[i]}"
                    else:
                        end_time = course_end_times[i]
                    entry = {
                            "id": 1,
                            "text": f"{course_code_list[i]} {start_time} - {end_time}{course_name_list[i]} {course_section_list[i]}",
                            "start": f"2013-03-25T{start_time}",
                            "end": f"2013-03-25T{end_time}",
                            "resource": resource,
                            "days": course_meeting_days[i]
                    }
                    return_list.append(entry)
                i = i + 1
            print(return_list)
            return json.dumps(return_list)
    data = json.dumps(
        []
    )
    return data

@app.route("/api/existingSchedule", methods=["POST"])
def get_existing_schedule():
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        global schedule_name
        schedule_name = json_data.get("name").rstrip()
        return "good"
    else:
        return "blah"

@app.route("/api/degreereport", methods=["GET", "POST"])
def degree_report():
    if request.method == "GET":
        global user_email
        degreeIds = report.getStudentMajors(user_email)
        
        studentDegreeReqs = report.getMajorRequirements(degreeIds[0][0])

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
