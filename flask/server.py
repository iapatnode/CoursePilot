from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os, re, json
from datetime import datetime
from mysql.connector import connect, Error
import AutoGenerateSchedule as AGS
import MinorRecomendation as MinorRecommendation
import dbQueries as db_queries
import degreeReport as report


#Which users are logged in

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
/API/LOGIN ROUTE
-----------------
This is the route that handles requests sent from the login page. If
the user sends a post request, get the email and the password contained
in the form of the request. Check to see if the user exists in the database. 

If the user is valid, reroute them to the home page. If they are not a valid
user, redirect them back to the login page. 
"""
@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        email = json_data.get("email")
        password = json_data.get("password")
        valid = True
        cont = True
        return_message = ""

        #Check to see that a valid email was entered
        if email is None or email == "":
            valid = False
            if cont:
                return_message = "Error: Email and password cannot be blank"
                cont = False
        else:
            domain = re.search("@[\w.]+", email)
            if domain.group() != '@gcc.edu':
                valid = False
                if cont:
                    return_message = "Error: Must use GCC email"
                    cont = False
        
        #Check to see that a password was entered
        if password is None or password == "":
            valid = False
            if cont:
                return_message = "Error: Email and Password cannot be blank"
                cont = False
        
        #Checks if student's credentials are in the database
        if valid:
            cursor = conn.cursor(buffered=True)
            studentQuery = "select * from Student where email = %s and binary passwrd = %s"
            studentCredentials = (email, password)

            try:
                cursor.execute(studentQuery, studentCredentials)
                conn.commit()

                #Checks if user with credentials exists
                if cursor.rowcount == 0:
                    valid = False
                    return_message = f"Error: Incorrect email or password detected"
                
            except Error as error:
                valid = False
            
            #DBMS connection cleanup
            cursor.close()

        if valid:
            return {
                "text": "success"
            }
        
        #If the user's credentials are not found, redirect them back to the login page
        else:
            return {
                "text": return_message
            }


"""
/API/SIGNUP
------------
This is the route that handles requests sent from the signup page. 

GET: When a get request is received, run a query that gets a list of all
     majors and minors that the user can select from and return them to 
     be displayed on the page. 

POST: When a post request is received, get all of the user information that
      is present in the form. If there is missing or invalid information, 
      redirect the user back to the signup page, else, create the user
      account and redirect them to the home page. 
"""
@app.route("/api/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        # On a post request, get all user data from the form received. 
        valid = True
        cont = True
        return_message = ""
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        email = json_data.get("email")
        password = json_data.get("password")
        confirm_password = json_data.get("confirm_password")
        requirement_year = json_data.get("requirement_year")
        graduation_year = json_data.get("graduation_year")
        major = json_data.get("major")
        minor = json_data.get("minor")

        #Check to see that the user gives a valid gcc email address
        if email is None or email == "":
            valid = False
            cont = False
            return_message = "Error: Email is a required field"
        if not "@" in email:
            valid = False
            if cont:
                return_message = "Error: Enter a valid email address"
                cont = False
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            domain = re.search("@[\w.]+", email)
            if domain.group() != '@gcc.edu':
                valid = False
                if cont:
                    return_message = "Error: A GCC email address is required"
                    cont = False
        
        # #Check to see whether or not the user gave a valid username
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        #Check to see if the user gave a valid password
        if len(password) < 8:
            valid = False
            if cont:
                return_message = "Error: Password must be at least 8 characters long"
                cont = False

        password_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)")
        if(password_regex.search(password)) == None:
            valid = False
            if cont:
                return_message = "Error: Password must contain uppercase/lowercase characters, numbers, and one special character"
                cont = False
            
        if(string_check.search(password) == None):
            valid = False
            if cont:
                return_message = "Error: Password must contain uppercase/lowercase characters, numbers, and one special character"
                cont = False
        
        #Check to see if the two password fields match
        if password != confirm_password:
            valid = False
            if cont:
                return_message = "Error: Two password fields must match"
                cont = False

        #Check to see that the user's major/minor selections are valid
        if major is None or major == []:
            valid = False
            if cont:
                return_message = "Error: You must select a major"
                cont = False

        if valid:
            # conn = connection()
            cursor = conn.cursor()
            newStudentQuery = "Insert into Student values (%s, %s, %s)"
            newStudentData = (email, password, graduation_year)

            #adds student and his/her info to the database
            try:
                cursor.execute(newStudentQuery, newStudentData)

                conn.commit()
            except Error as error:
                #If you cannot insert the invidual into the database, print error and reroute
                return redirect("http//localhost:3000/SignUp")
            
            #Adds student major and minor information to database
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
                        conn.commit()
                
                for mm in minor:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (mm, requirement_year, 1))
                    result = cursor.fetchall()
                    for row in result:
                        mid = row[0]
                    
                        addToMinor = "insert into StudentMajorMinor values (%s, %s)"
                        cursor.execute(addToMinor, (email, mid))
                        conn.commit()
            
            except Error as error:
                #If you cannot insert the major/minor into the database, print error and reroute
                return redirect("http//localhost:3000/SignUp")

            #DBMS connection cleanup
            cursor.close()

            user_email = email

            return {
                "text": return_message
            }
        else:
            return {
                "text": return_message
            }

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


"""
/API/HOME
----------
This is the route that handles all requests sent from the home page.

GET: When a get request is received, we run a query that gets all of the schedule information
     for the user that is currently logged in. This data is returned and displayed on the home
     page. 

POST: When a post request is received, we know that the user is trying to make a new schedule. 
      We get the name and semester of the schedule from the request form, and attempt to insert
      the information into our database. If the schedule is a duplicate or cannot be entered, 
      we catch an error. 
"""
@app.route("/api/home", methods=["GET", "POST"])
def home():
    # Variable to tell which user is logged in and what semester they have selected for their schedule
    semester_selection = request.args.get("semester")
    user_email = request.args.get("email")
    if request.method == "GET":
        all_schedules = []
        cursor = conn.cursor()

        # Get user schedules from the database
        get_schedules_query = ('''
            SELECT * FROM Schedule WHERE email = %s;
            ''')
        cursor.execute(get_schedules_query, (user_email,))
        result = cursor.fetchall()

        # For each schedule received, append it's information to the list that is returned
        for schedule in result:
            all_schedules.append(
                {
                    "scheduleName": schedule[0],
                    "dateModified": str(schedule[1]),
                    "email": schedule[2],
                    "scheduleSemester": schedule[3]
                }
            )
        # Return schedule information
        return json.dumps(all_schedules)

    if request.method == "POST":
        cursor = conn.cursor()

        # Get schedule name and semester from the request form
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        schedule_name = json_data.get("schedule-name")
        schedule_semester = json_data.get("schedule-semester")
        semester_selection = json_data.get("schedule-semester")
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

        # Attempt to insert the new schedule into the database. 
        insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
        cursor.execute(insert_schedule_query, (schedule_name, formatted_date, user_email, schedule_semester))
        conn.commit()

        return "Created Schedule Successfully"


@app.route("/api/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search_val = ""
        search_val = request.form.get("outlined-search")
        cursor = conn.cursor()
        classArray = []
        courseArray = []

        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
        ''', (f"%{(search_val)}%",))

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
            }
            courseArray.append(course_dict)

            for item in row:
                result_string += str(item)

        return json.dumps(courseArray)


"""
/API/SCHEDULE
---------------
This is the route that handles all of the requests for the schedule page

GET: When a get request is received, the route returns all of the class
     information for courses available in the semester the user chose
    
POST: When a post request is received, the route takes all of the courses that 
      the user has added to their schedule and attempts to add them to the database, 
      thus saving the schedule. 
"""
@app.route('/api/schedule', methods=["GET", "POST"])
def schedule():
    semester_selection = request.args.get("semester")
    user_email = request.args.get("email")
    schedule_name = request.args.get("ScheduleName")

    if request.method == "GET":
        cursor = conn.cursor()
        classArray = []
        courseArray = []

        
        # Select the schedule that the user has created
        cursor.execute('''
            SELECT scheduleSemester from Schedule WHERE scheduleName = %s AND email = %s;
            ''', (schedule_name, user_email,))

        semester = cursor.fetchall()
        semester_current = ""

        # Get the semester of the selected schedule
        for result in semester:
            semester_current = result[0]

        # Get all of the courses that are available for the semester that the student chose
        cursor.execute(''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode WHERE
             (classSemester = %s or classSemester = %s or classSemester = %s) order by Course.courseCode;
            ''', (semester_current, "both", "alternate",))

        class_table = cursor.fetchall()

        result_string = ""

        # For every course retrieved, add the following information to a dictionary to return
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

        # Return all course information
        return json.dumps(courseArray)
    
    if request.method == "POST":
        cursor = conn.cursor()
        # Update the time that the schedule was last modified
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')
        update_schedule = "UPDATE Schedule SET dateModified = %s where scheduleName = %s and email = %s"
        cursor.execute(update_schedule, (formatted_date, schedule_name, user_email,))

        return_text = ""

        # Get data from the semester form that the user submitted
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        code_pt_1 = ""
        code_pt_2 = ""
        section = ""
        codes = []
        sections = []
        classes = []

        #Delete courses that were removed from the schedule
        for course in json_data.get("removed"):
            delete_query = "delete from ScheduleClass where email = %s and scheduleName = %s and courseCode = %s"
            cursor.execute(delete_query, (user_email, schedule_name, course))
        conn.commit()

        #Get the appropriate semester from the Schedule table
        cursor.execute('''
            SELECT scheduleSemester from Schedule WHERE scheduleName like %s AND email like %s;
            ''', (f"%{(schedule_name)}%", f"%{(user_email)}%",))

        semester = cursor.fetchall()

        #Do some formatting with the strings to get course name, codes, etc...
        if json_data.get("courses"):
            for course in json_data.get("courses"):
                course_string = course.replace(" ", "-")
                index = course_string.index('-')
                code_pt_1 = course_string[0: index + 4]
                section = course[-1]
                code = code_pt_1.replace("-", " ")
                course_w_section = f"{code} {section}"
                codes.append(code)
                sections.append(section)

                #Get class info from Class table using code and section as keys
                cursor.execute(''' 
                    SELECT * from Class WHERE courseCode like %s AND courseSection like %s and classSemester = %s;
                    ''', (f"%{(code)}%", f"%{(section)}", semester_selection,))
                schedule_class = cursor.fetchall()

                # Insert all courses that the student added into the database. 
                for row in schedule_class:
                    classInsert = """INSERT into ScheduleClass 
                        (scheduleName, email, courseSection, courseCode, meetingDays, classSemester, startTime, endTime)
                        values (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(classInsert, (schedule_name, user_email, row[0], row[5], row[4], row[1], row[2], row[3],))
                conn.commit()
            
            # Prerequisite checking
            prerequisite_query = "select * from Prerequisite where courseCode like %s"
            all_classes_query = "select * from ScheduleClass where scheduleName = %s and email = %s"

            # Get a list of all courses that the user has taken, append to a list
            user_taken_courses_query = "select * from StudentCourses where email = %s"
            cursor.execute(user_taken_courses_query, (user_email,))
            user_taken_courses = cursor.fetchall()
            user_courses_list = []
            for course in user_taken_courses:
                user_courses_list.append(course[1])

            cursor.execute(all_classes_query, (schedule_name, user_email,))
            all_classes = cursor.fetchall()

            # Based on the courses that the user has taken, check to see if they have fulfilled prereqs. 
            failed_prereq = []
            for ind_class in all_classes:
                name = ind_class[3]
                cursor.execute(prerequisite_query, (name,))
                prerequisites = cursor.fetchall()
                group = 1
                temp_list = []
                for prereq in prerequisites:
                    if prereq[0] == group:
                        temp_list.append(prereq[1])
                    else:
                        return_text = ""
                        for prerequisite in temp_list:
                            if prerequisite not in user_courses_list:
                                return_text = "Warning: You have not taken all necessary prerequites for the following courses on your schedule"
                                failed_prereq.append(ind_class[3])
                        group = group + 1
                        temp_list = []
                        temp_list.append(prereq[1])
                    
                # For each of the prereqs for each course the user added, warn them if they have not taken the prereq
                for prerequisite in temp_list:
                    if prerequisite not in user_courses_list:
                        return_text = "Warning: You have not taken all necessary prerequites for the following courses on your schedule"
                        failed_prereq.append(ind_class[3])

                if return_text == "":
                    return_text = "Saved Schedule Successfully"
            seen_courses = []
            i = 1
            for course in failed_prereq:
                if not course in seen_courses:
                    seen_courses.append(course)
                    return_text = return_text + f"\n{i}. {course}"
                    i = i + 1
            return f"{return_text}"
    return "Successfully Saved Schedule"


"""
/API/DELETE
------------
This is the route that handles the user deleting a schedule

POST: When the user posts to this endpoint, the following code removed
      all courses from the user's schedule that they selected to delete, 
      as well as deleting the schedule itself from the database. 
"""
@app.route("/api/delete", methods=["POST"])
def delete_schedule():
    schedule_name = request.args.get("ScheduleName")
    user_email = request.args.get("email")
    cursor = conn.cursor()
    cursor.execute('''
        delete from ScheduleClass WHERE email like %s AND scheduleName like %s;
    ''', (f"%{(user_email)}%", f"{(schedule_name)}",))

    cursor.execute('''
        delete from Schedule WHERE email like %s AND scheduleName like %s;
    ''', (f"%{(user_email)}%", f"{(schedule_name)}",))

    conn.commit()
    return "success"


"""
/API/COMPARE
--------------
This is the route that handles requests to compare two schedules

POST: When the user sends a post request to this url, we set two variables indicating
      which schedules that the user has chosen to compare, and redirect the user
      to the compare page. 
"""
@app.route("/api/compare", methods=["POST"])
def compare_schedules():
    cursor = conn.cursor()
    if request.method == "POST":
        data = request.form
        compare_schedule_one = request.args.get('scheduleOne')
        compare_schedule_two = data.get('schedule')
        return redirect("http://localhost:3000/compare")
    return ""


"""
/API/LOADCOMPAREDSCHEDULES
----------------------------
This is the route that handles loading in the class events for two schedules we are comparing

GET: When the user sends a get request, we execute a query that loads all of the class events
     for the two schedules that the user chose to compare. We then return this list of 
     dictionaries to the compare page to be displayed to the user. 
"""
@app.route("/api/loadComparedSchedules", methods=["GET", "POST"])
def get_data_compare():
    cursor = conn.cursor()
    if request.method == "POST" or request.method == "GET":
        return_list = []
        course_codes = []
        compare_schedule_one = request.args.get("scheduleOne")
        compare_schedule_two = request.args.get("scheduleTwo")
        user_email = request.args.get("email")
        user_email = user_email[6:]
        semester_selection = "fall"
        schedule_name = "bruh"
        backColor = ""

        # Make sure that the user did not only select one schedule to compare. 
        if schedule_name != "" or schedule_name == "":
            # Get all courses in the two selected schedules
            schedule_info_query = "select * from ScheduleClass where scheduleName = %s or scheduleName = %s and email = %s"
            cursor.execute(schedule_info_query, (compare_schedule_one, compare_schedule_two, user_email,))
            results = cursor.fetchall()

            # For each class gotten, set the background colors of the calendar events according to which schedule they are apart of
            for row in results:
                if row[0] == compare_schedule_one:
                    backColor = "#926DD6"
                else:
                    backColor = "#d89cf6"
                
                start_time = ""
                end_time = ""
                # For each class in the loaded schedule list, create a calendar event
                # for the course, meaning set the days, start and end time, and event
                # title. 
                if row[3] not in course_codes or row[3] in course_codes:
                    count = 0
                    if row[3] in course_codes:
                        for course in course_codes:
                            if course == row[3]:
                                count = count + 1
                    if count <= 1:
                        count = 0
                        course_codes.append(row[3])
                        start_time = str(row[6])
                        end_time = str(row[7])
                        if(len(start_time) < 8):
                            start_time = f"0{start_time}"
                        if(len(end_time) < 8):
                            end_time = f"0{end_time}"
                        for day in row[4]:
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
                            entry = {
                                    "id": 1,
                                    "text": f"{row[3]}",
                                    "start": f"2013-03-25T{start_time}",
                                    "end": f"2013-03-25T{end_time}",
                                    "resource": resource,
                                    "days": row[4],
                                    "backColor": backColor
                            }
                            return_list.append(entry)
                # This else statement is needed for classes who have labs, where
                # we want to make sure we do not overlook a lab section just because
                # it has the same course code (i.e. look at the section to see if it's a lab)
                else:
                    if row[2] >= "L":
                        course_codes.append(row[3])
                        start_time = str(row[6])
                        end_time = str(row[7])
                        if(len(start_time) < 8):
                            start_time = f"0{start_time}"
                        if(len(end_time) < 8):
                            end_time = f"0{end_time}"
                        for day in row[4]:
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
                            entry = {
                                    "id": 1,
                                    "text": f"{row[3]}",
                                    "start": f"2013-03-25T{start_time}",
                                    "end": f"2013-03-25T{end_time}",
                                    "resource": resource,
                                    "days": row[4]
                            }
                            return_list.append(entry)
            # Return the list of class events. 
            return json.dumps(return_list)
    data = json.dumps(
        []
    )
    return data


@app.route("/api/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        user_email = request.args.get("email")
        passwrd = ""
        majors = []
        minors = []
        cursor = conn.cursor()
        user_info = ''' SELECT Student.email, StudentMajorMinor.degreeId, Student.passwrd FROM Student join StudentMajorMinor on Student.email = StudentMajorMinor.email where Student.email = %s; '''
        cursor.execute(user_info, (user_email,))
        results = cursor.fetchall()
        for result in results:
            id = result[1]
            check_if_major_or_minor = ''' select MajorMinor.isMinor, MajorMinor.degreeName from MajorMinor where MajorMinor.degreeId = %s '''
            cursor.execute(check_if_major_or_minor, (id,))
            status = cursor.fetchall()
            for row in status:
                if row[0] == 1:
                    minors.append(row[1])
                else:
                    majors.append(row[1])
            passwrd = result[1]
        # conn.commit()
        password_query = "select passwrd from Student where email = %s"
        cursor.execute(password_query, (user_email,))
        results = cursor.fetchone()
        passwrd = results[0]
        return {
            "email": user_email,
            "majors": majors, 
            "minors": minors,
            "passwrd": passwrd,
        }


@app.route("/api/changeMajor", methods=["POST"])
def changeMajor():
    cursor = conn.cursor()
    valid = True
    user_email = request.args.get("email")
    data = request.data.decode("utf-8")
    json_data = json.loads(data)
    major = json_data.get("major")
    minors = []
    if major is None or major == []:
        valid = False
    
    else:
        """
        Workflow:
        1. Get all student major minor details. 
        2. For each entry, search MajorMinor database and determine whether it is a minor or not
        3. If it is a minor, add to list of minors, continue
        4. Delete all student major minor info
        5. Add all new major info
        6. Add back all minor info
        7. Commit
        """
        try:
            # Workflow 1: Get all student major minor details
            getMinorQuery = """
                select * from StudentMajorMinor join MajorMinor on StudentMajorMinor.degreeId = MajorMinor.degreeID
                where StudentMajorMinor.email = %s;
            """
            cursor.execute(getMinorQuery, (user_email,))
            results = cursor.fetchall()
            # Workflow 2/3: Search each entry in major minor database to determine whether the id represents a minor, add to list
            for result in results:
                isMinor = result[4]
                if(result[4]) == 1:
                    minors.append(result[1])

            # Workflow 4: Delete StudentMajorMinor info
            deleteStudentDegree = "delete from StudentMajorMinor where email = %s"
            cursor.execute(deleteStudentDegree, (user_email,))
            conn.commit()

            # Workflow 5: Add back new major info
            studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"
            for m in major:
                mid = 0
                cursor.execute(studentDegreeQuery, (m, 2017, 0))
                result = cursor.fetchall()
                for row in result:
                    mid = row[0]
                    addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                    cursor.execute(addToMajorMinor, (user_email, mid))
                    conn.commit()
                
            # Workflow 6: Add back minor info
            for minor in minors:
                addMinors = "insert into StudentMajorMinor values (%s, %s)"
                cursor.execute(addMinors, (user_email, minor))
                conn.commit()
            
            # Delete courses that Student has taken (fixes bug in Degree report)
            delete_courses_query = "delete from StudentCourses where email = %s"
            cursor.execute(delete_courses_query, (user_email,))
            conn.commit()

        except Error as error:
            #If you cannot insert the invidual into the database, print error and reroute
            return redirect("http//localhost:3000/Profile")

    return "good"

@app.route("/api/changeMinor", methods=["POST"])
def changeMinor():
    cursor = conn.cursor()
    valid = True
    requirement_year = 2017
    user_email = request.args.get("email")
    data = request.data.decode("utf-8")
    json_data = json.loads(data)
    minor = json_data.get("minor")
    majors = []
    if minor is None or minor == []:
        valid = False
    
    else:
        """
        Workflow:
        1. Get all student major minor details. 
        2. For each entry, search MajorMinor database and determine whether it is a minor or not
        3. If it is a minor, add to list of minors, continue
        4. Delete all student major minor info
        5. Add all new major info
        6. Add back all minor info
        7. Commit
        """
        try:
            # Workflow 1: Get all student major minor details
            getMajorQuery = """
                select * from StudentMajorMinor join MajorMinor on StudentMajorMinor.degreeId = MajorMinor.degreeID
                where StudentMajorMinor.email = %s;
            """
            cursor.execute(getMajorQuery, (user_email,))
            results = cursor.fetchall()
            # Workflow 2/3: Search each entry in major minor database to determine whether the id represents a minor, add to list
            for result in results:
                isMajor = result[4]
                if(result[4]) == 0:
                    majors.append(result[1])

            # Workflow 4: Delete StudentMajorMinor info
            deleteStudentDegree = "delete from StudentMajorMinor where email = %s"
            cursor.execute(deleteStudentDegree, (user_email,))
            conn.commit()

            # Workflow 5: Add back new minor info
            studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"
            for m in minor:
                mid = 0
                cursor.execute(studentDegreeQuery, (m, 2017, 1))
                result = cursor.fetchall()
                for row in result:
                    mid = row[0]
                    addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                    cursor.execute(addToMajorMinor, (user_email, mid))
                    conn.commit()
                
            # Workflow 6: Add back minor info
            for major in majors:
                addMinors = "insert into StudentMajorMinor values (%s, %s)"
                cursor.execute(addMinors, (user_email, major))
                conn.commit()

        except Error as error:
            #If you cannot insert the invidual into the database, print error and reroute
            return redirect("http//localhost:3000/Profile")

    return "good"

@app.route("/api/changePassword", methods=["POST"])
def changePassword():
    data = request.data.decode("utf-8")
    json_data = json.loads(data)
    oldPassword = json_data.get("oldPassword")
    newPassword = json_data.get("newPassword")
    user_email = request.args.get("email")
    valid = False
    cursor = conn.cursor()
    getUserPassword = "select passwrd from Student where email = %s"
    cursor.execute(getUserPassword, (user_email,))
    results = cursor.fetchone()
    password = results[0]
    if password == oldPassword:
        valid = True
    if valid:
        updateUserPassword = "update Student set passwrd = %s where email = %s"
        cursor.execute(updateUserPassword, (newPassword, user_email,))
        conn.commit()
        return  "success"
    else:
        return "error"
    
    
"""
/API/GETSCHEDULEINFO
----------------------
This is the route that handles getting schedule info, such as courses and times, 
and adds them to the schedule when a user selects a pre-existing schedule

GET: The user can only send get requests to this URL. When they do, similar
     to the load compared schedules endpoint, we get all of the courses saved
     under the selected schedule, and return the class events to be displayed. 
"""
@app.route("/api/getScheduleInfo", methods=["GET"])
def get_new_schedule():
    cursor = conn.cursor()
    if request.method == "GET":
        return_list = []
        course_codes = []

        schedule_name = request.args.get("ScheduleName")
        user_email = request.args.get("email")

        # Make sure the user entered a schedule name, get all courses in that schedule
        if schedule_name != "":
            schedule_info_query = "select * from ScheduleClass where email = %s and scheduleName = %s"
            cursor.execute(schedule_info_query, (user_email, schedule_name,))
            results = cursor.fetchall()
            # For every course in the results, create a calendar event and return the end list
            for row in results:
                start_time = ""
                end_time = ""
                if row[3] not in course_codes:
                    course_codes.append(row[3])
                    start_time = str(row[6])
                    end_time = str(row[7])
                    if(len(start_time) < 8):
                        start_time = f"0{start_time}"
                    if(len(end_time) < 8):
                        end_time = f"0{end_time}"
                    for day in row[4]:
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
                        entry = {
                                "id": 1,
                                "text": f"{row[3]}",
                                "start": f"2013-03-25T{start_time}",
                                "end": f"2013-03-25T{end_time}",
                                "resource": resource,
                                "days": row[4],
                                "backColor": "#926DD6"
                        }
                        return_list.append(entry)
                else:
                    if row[2] >= "L":
                        course_codes.append(row[3])
                        start_time = str(row[6])
                        end_time = str(row[7])
                        if(len(start_time) < 8):
                            start_time = f"0{start_time}"
                        if(len(end_time) < 8):
                            end_time = f"0{end_time}"
                        for day in row[4]:
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
                            entry = {
                                    "id": 1,
                                    "text": f"{row[3]}",
                                    "start": f"2013-03-25T{start_time}",
                                    "end": f"2013-03-25T{end_time}",
                                    "resource": resource,
                                    "days": row[4],
                                    "backColor": "#926DD6"
                            }
                            return_list.append(entry)
            return json.dumps(return_list)
    # If there was an error with any of the above conditions, return an empty list (no classes)
    data = json.dumps(
        []
    )
    return data


"""
/API/EXISTINGSCHEDULE
-----------------------
This is the endpoint that handles the user selecting an existing schedule to load 
and view. 

POST: The user can only send a post request to this URL. When they do, we save the name
      of the schedule that they chose, so we can load in all the class events when they
      are redirected to the schedule page. 
"""
@app.route("/api/existingSchedule", methods=["POST"])
def get_existing_schedule():
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = json.loads(data)
        schedule_name = json_data.get("name").rstrip()
        return "good"
    else:
        return "blah"

@app.route("/api/degreereport", methods=["GET", "POST"])
def degree_report():
    user_email = request.args.get("email")

    if request.method == "GET":

        degreeIds = report.getStudentMajors(user_email)
        studentDegreeReqs = report.getMajorRequirements(degreeIds[0][0])

        studentCourses = report.getStudentCourses(user_email)

        studentReqDetails = [studentDegreeReqs, studentCourses]

        return json.dumps(studentReqDetails)
        
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = json.loads(data)

        addCourses = json_data.get("add")
        deleteCourses = json_data.get("remove")

        report.insertStudentCourses(user_email, addCourses)
        report.deleteStudentCourses(user_email, deleteCourses)

        return redirect(f"http://localhost:3000/degreereport?email={user_email}")




@app.route("/api/autoGenerate", methods=["GET", "POST"])
def autoGenerate():
    #TODO: Return user data retrieved from database tables as needed
    user_email = request.args.get("email")
    semester_selection = request.args.get("semester")
    schedule_name = request.args.get("name")
    if request.method == "GET":
        all_schedules = []
        cursor = conn.cursor()
        get_schedules_query = ('''
            SELECT * FROM Schedule WHERE email = %s;
            ''')
        cursor.execute(get_schedules_query, (user_email,))
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
        return json.dumps(all_schedules)

    if request.method == "POST":
        cursor = conn.cursor()
        schedule_name = request.form.get("schedule-name")
        schedule_semester = request.form.get("schedule-semester")
        semester_selection = request.form.get("schedule-semester")
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')
        session["schedule_semester"] = schedule_semester #Test to load courses and whatnot

        insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
        cursor.execute(insert_schedule_query, (schedule_name, formatted_date, user_email, schedule_semester))
        conn.commit()

        semester = semester_selection

        RecommendedCourses = AGS.GetAutoGeneratedSchedule(user_email, semester)

        for course in RecommendedCourses:
            classInsert = "INSERT into ScheduleClass (scheduleName, email, courseSection, courseCode, meetingDays, classSemester, startTime, endTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(classInsert, (schedule_name, user_email, course.courseSection, course.courseCode, course.dayAvail, course.semesterAvail, course.startTime, course.endTime))
            conn.commit()




        schedule_url = f"http://localhost:3000/Schedule?email={user_email}&ScheduleName={schedule_name}"

        return redirect(schedule_url)

@app.route("/api/getAllMajorsAndMinors", methods=["GET"])
def getAllMajorsAndMinors():
    user_email = request.args.get("email")
    all = MinorRecommendation.getEverythingJSON(user_email)
    return json.dumps(all)
