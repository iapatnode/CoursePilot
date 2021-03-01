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

#User Email Variable
user_email = ""

#Semester Selection Variable
semester_selection = ""

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
            print(schedule)
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

        return redirect(url)

@app.route("/api/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search_val = ""
        search_val = request.form.get("outlined-search")
        cursor = conn.cursor()
        classArray = []
        courseArray = []
        #request_json = request.get_json()
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
        cursor = conn.cursor()
        classArray = []
        courseArray = []
        print("Selected:" + semester_selection)
        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode WHERE courseSemester like %s order by Course.courseCode;
            ''', (f"%{(semester_selection)}%",))


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
                # print(row)
                result_string += str(item)

        for row in classArray:
            print(row)

        return json.dumps(courseArray)
    
    if request.method == "POST":
        cursor = conn.cursor()
        data = request.data.decode("utf-8")
        print("data: ")
        print(data)
        json_data = json.loads(data)
        code_pt_1 = ""
        code_pt_2 = ""
        section = ""
        codes = []
        sections = []
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

            cursor.execute(''' 
            SELECT * from Class WHERE courseCode like %s AND courseSection like %s;
            ''', (f"%{(code)}%", f"%{(section)}",))

            schedule_class = cursor.fetchall()
            print("this is from the database")
            print(schedule_class)
        
        #TODO: Iterate over all of the codes and sections, add them to the database


        # print(f"{codes}{sections}")
        return f"{codes} {sections}"


@app.route("/api/getScheduleInfo", methods=["GET"])
def get_new_schedule():
    data = json.dumps(
        []
    )

    return data








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
