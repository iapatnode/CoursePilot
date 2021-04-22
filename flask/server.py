from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os, re, json
from datetime import datetime
from mysql.connector import connect, Error
import MinorRecomendation as MinorRecommendation
import string
import random

#NEED TO TEST!!!!


#Which users are logged in
user_dict = {}

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
                print("Unable to execute query..." + str(error))
                valid = False
            
            #DBMS connection cleanup
            cursor.close()

        if valid:
            uid = ""
            if not email in user_dict:
                letters = string.ascii_letters
                uid = ''.join(random.choice(letters) for i in range(32))
                user_dict[email] = uid
            else:
                uid = user_dict[email]
            return {
                "text": uid
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
            cursor = conn.cursor()

            try:
                #adds student and his/her info to the database
                newStudentQuery = "Insert into Student values (%s, %s, %s)"
                newStudentData = (email, password, graduation_year)

                cursor.execute(newStudentQuery, newStudentData)

                #Adds student major and minor information to database
                studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"
                for m in major:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (m, requirement_year, 0))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        studentDegreeQuery = "select degreeId from MajorMinor where degreeName = %s and isMinor = %s"
                        cursor.execute(studentDegreeQuery, (m, 0))
                        result = cursor.fetchall()
                        for row in result:
                            mid = row[0]
                        
                    else:
                        for row in result:
                            mid = row[0]
                        
                    addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                    cursor.execute(addToMajorMinor, (email, mid))

                studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"
                for mm in minor:
                    mid = 0
                    cursor.execute(studentDegreeQuery, (mm, requirement_year, 1))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        studentDegreeQuery = "select degreeId from MajorMinor where degreeName = %s and isMinor = %s"
                        cursor.execute(studentDegreeQuery, (mm, 1,))
                        result = cursor.fetchall()
                        for row in result:
                            mid = result[0]
                    
                    else:
                        for row in result:
                            mid = row[0]
                    
                    addToMinor = "insert into StudentMajorMinor values (%s, %s)"
                    cursor.execute(addToMinor, (email, mid))
                conn.commit()
            
            except Error as error:
                #If you cannot insert the major/minor into the database, print error and reroute
                return redirect("http//coursepilot.gcc.edu:3000/SignUp")

            #DBMS connection cleanup
            cursor.close()

            uid = ""
            if not email in user_dict:
                letters = string.ascii_letters
                uid = ''.join(random.choice(letters) for i in range(32))
                user_dict[email] = uid
            return {
                "text": uid
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
    # Variable to tell which user is logged in
    user_email = request.args.get("email")
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
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
        created_at = datetime.now()
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

        # Attempt to insert the new schedule into the database. 
        insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
        cursor.execute(insert_schedule_query, (schedule_name, formatted_date, user_email, schedule_semester))
        conn.commit()

        return "Created Schedule Successfully"

#NOTE: NEEDS COMMENTS
@app.route("/api/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        search_val = ""
        search_val = request.form.get("outlined-search")
        cursor = conn.cursor()
        courseArray = []

        classCourseQuery = ''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode where Class.courseCode like %s;
        '''

        cursor.execute(classCourseQuery, (f"%{(search_val)}%",))

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
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
    schedule_name = request.args.get("ScheduleName")

    if request.method == "GET":
        cursor = conn.cursor()
        courseArray = []

        
        # Select the schedule that the user has created
        scheduleQuery = '''
            SELECT scheduleSemester from Schedule WHERE scheduleName = %s AND email = %s;
            '''
        cursor.execute(scheduleQuery, (schedule_name, user_email,))

        semester = cursor.fetchall()
        semester_current = ""

        # Get the semester of the selected schedule
        for result in semester:
            semester_current = result[0]

        # Get all of the courses that are available for the semester that the student chose
        courseQuery = ''' 
            SELECT * from Course join Class on Class.courseCode = Course.courseCode WHERE
             (classSemester = %s or classSemester = %s or classSemester = %s) order by Course.courseCode;
            '''
        cursor.execute(courseQuery, (semester_current, "both", "alternate",))

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
        added_courses = json_data.get("courses")
        removed_courses = json_data.get("removed")
        code_pt_1 = ""
        section = ""
        codes = []
        sections = []

        courses_in_schedule = True
        get_schedule_info = "select * from ScheduleClass where email = %s and scheduleName = %s"
        cursor.execute(get_schedule_info, (user_email, schedule_name,))
        results = cursor.fetchall()
        if len(results) == 0:
            courses_in_schedule = False

        if courses_in_schedule:
            #Delete courses that were removed from the schedule
            print(f"Removed Courses: {json_data.get('removed')}")
            for course in removed_courses:
                delete_query = "delete from ScheduleClass where email = %s and scheduleName = %s and courseCode = %s"
                cursor.execute(delete_query, (user_email, schedule_name, course))
            conn.commit()

        #Ger duplicate courses out of added courses
        already_removed = []
        for added in added_courses:
            for removed in removed_courses:
                if added == removed and removed not in already_removed:
                    already_removed.append(removed)
                    added_courses.remove(removed)

        #Get the appropriate semester from the Schedule table
        semesterScheduleQuery = '''
            SELECT scheduleSemester from Schedule WHERE scheduleName like %s AND email like %s;
            '''
        cursor.execute(semesterScheduleQuery, (f"%{(schedule_name)}%", f"%{(user_email)}%",))

        semester = cursor.fetchall()

        #Do some formatting with the strings to get course name, codes, etc...
        print(f"Added: {json_data.get('courses')}")
        if json_data.get("courses"):
            for course in added_courses:
                print(f"Course: {course}")
                course_string = course.replace(" ", "-")
                index = course_string.index('-')
                code_pt_1 = course_string[0: index + 4]
                section = course[-1]
                code = code_pt_1.replace("-", " ")
                codes.append(code)
                sections.append(section)

                #Get class info from Class table using code and section as keys
                classCodeSectionQuery = ''' 
                    SELECT * from Class WHERE courseCode like %s AND courseSection like %s and (classSemester = %s or classSemester = %s or classSemester = %s);
                    '''
                cursor.execute(classCodeSectionQuery, (f"%{(code)}%", f"%{(section)}", semester_selection, "alternate", "both"))
                schedule_class = cursor.fetchall()
                print(f"{code} {semester_selection}")

                # Insert all courses that the student added into the database. 
                for row in schedule_class:
                    print("Made it inside the loop")
                    classInsert = """INSERT into ScheduleClass 
                        (scheduleName, email, courseSection, courseCode, meetingDays, classSemester, startTime, endTime)
                        values (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(classInsert, (schedule_name, user_email, row[0], row[5], row[4], row[1], row[2], row[3],))
                    print(f"Successfully added {row[5]}")
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
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
    cursor = conn.cursor()
    deleteClassQuery = '''
        delete from ScheduleClass WHERE email like %s AND scheduleName like %s;
    '''
    cursor.execute(deleteClassQuery, (f"%{(user_email)}%", f"{(schedule_name)}",))

    deleteScheduleQuery = '''
        delete from Schedule WHERE email like %s AND scheduleName like %s;
    '''
    cursor.execute(deleteScheduleQuery, (f"%{(user_email)}%", f"{(schedule_name)}",))

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
    if request.method == "POST":
        data = request.form
        compare_schedule_one = request.args.get('scheduleOne')
        compare_schedule_two = data.get('schedule')
        return redirect("http://coursepilot.gcc.edu:3000/compare")
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
        global user_dict
        for entry in user_dict: 
            if user_dict[entry] == user_email:
                user_email = entry
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

#NOTE: NEEDS COMMENTS
@app.route("/api/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        user_email = request.args.get("email")
        global user_dict
        for entry in user_dict: 
            if user_dict[entry] == user_email:
                user_email = entry
        passwrd = ""
        majors = []
        minors = []
        cursor = conn.cursor()
        user_info = ''' SELECT Student.email, StudentMajorMinor.degreeId, Student.passwrd FROM Student join StudentMajorMinor 
                        on Student.email = StudentMajorMinor.email where Student.email = %s; '''
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
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
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
                if(result[4]) == 1:
                    minors.append(result[1])

            # Workflow 4: Delete StudentMajorMinor info
            deleteStudentDegree = "delete from StudentMajorMinor where email = %s"
            cursor.execute(deleteStudentDegree, (user_email,))
            conn.commit()

            # Workflow 5: Add back new major info
            studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and isMinor = %s"
            for m in major:
                mid = 0
                cursor.execute(studentDegreeQuery, (m, 0))
                result = cursor.fetchall()
                i = 0
                for row in result:
                    if i < 1:
                        mid = row[0]
                        addToMajorMinor = "insert into StudentMajorMinor values (%s, %s)"
                        cursor.execute(addToMajorMinor, (user_email, mid))
                        i = i + 1
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
            return redirect("http//coursepilot.gcc.edu:3000/Profile")

    return "success"

#NOTE: NEEDS COMMENTS
@app.route("/api/changeMinor", methods=["POST"])
def changeMinor():
    cursor = conn.cursor()
    valid = True
    user_email = request.args.get("email")
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
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
            return redirect("http//coursepilot.gcc.edu:3000/Profile")

    return "success"

@app.route("/api/changePassword", methods=["POST"])
def changePassword():
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = ""
        try:
            json_data = json.loads(data)
        except Error as error:
            return "error"
        oldPassword = json_data.get("oldPassword")
        newPassword = json_data.get("newPassword")
        user_email = request.args.get("email")
        global user_dict
        for entry in user_dict: 
            if user_dict[entry] == user_email:
                user_email = entry
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
    
@app.route("/api/logout", methods=["POST"])
def logout():
    user_email = request.args.get("email")
    global user_dict
    email = ""
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            email = entry
    if entry != "":
        del user_dict[entry]
    return {
        "text": "success"
    }

    
    
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
        global user_dict
        for entry in user_dict: 
            if user_dict[entry] == user_email:
                user_email = entry

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
        return "success"
    else:
        return "error"

'''
/API/DEGREEREPORT
-------------------
This is the endpoint that handles the user adding and removing courses from the Degree Report page

GET: sets up the Degree report page with the necessary information about the database from the student: 
     degree name, requirement categories, requirement courses, courses completed

POST: The user sends a post request when they submit the form that is the Degree Report page. When they
      do, the courses that they have selected are added to the database (if not yet in the datase) and
      the courses they have unmarked are removed from the database (if in the database)
'''
@app.route("/api/degreereport", methods=["GET", "POST"])
def degree_report():
    user_email = request.args.get("email")
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry

    if request.method == "GET":
        # Gets the ids of all majors of the students
        degreeIds = getStudentMajors(user_email)

        # Gets the degree details of the first major of the student
        studentDegreeReqs = getMajorRequirements(degreeIds[0][0])

        # Gets all courses in the database
        courses = getAllCourses()

        # Gets all courses the student has taken: parsed into selected courses and checked courses
        parsedCourses = parseStudentCourses(user_email, studentDegreeReqs)

        studentReqDetails = [studentDegreeReqs, courses, parsedCourses]

        return json.dumps(studentReqDetails)
        
    if request.method == "POST":
        data = request.data.decode("utf-8")
        json_data = json.loads(data)

        addCheckedCourses = json_data.get("checkedAdd")
        addSelectedCourses = json_data.get("selectedAdd")
        deleteCheckedCourses = json_data.get("checkedRemove")
        deleteSelectedCourses = json_data.get("selectedRemove")

        # Adds completed courses to the database
        insertStudentCourses(user_email, addCheckedCourses)
        insertStudentCourses(user_email, addSelectedCourses)

        # Removes now incompleted courses from the database
        deleteStudentCourses(user_email, deleteCheckedCourses)
        deleteStudentCourses(user_email, deleteSelectedCourses)

        return redirect(f"http://coursepilot.gcc.edu:3000/api/degreereport?email={user_email}")

#NOTE: NEEDS COMMENTS
@app.route("/api/autoGenerate", methods=["GET", "POST"])
def autoGenerate():
    # Return user data retrieved from database tables as needed
    user_email = request.args.get("email")
    uid = user_email
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
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

        try:
            insert_schedule_query = "INSERT INTO Schedule values (%s, %s, %s, %s)"
            cursor.execute(insert_schedule_query, (schedule_name, formatted_date, user_email, schedule_semester))
            conn.commit()
        except Exception:
            return redirect(f"http://coursepilot.gcc.edu:3000/Home?email={uid}")

        semester = semester_selection

        RecommendedCourses = GetAutoGeneratedSchedule(user_email, semester)

        for course in RecommendedCourses:
            classInsert = "INSERT into ScheduleClass (scheduleName, email, courseSection, courseCode, meetingDays, classSemester, startTime, endTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(classInsert, (schedule_name, user_email, course.courseSection, course.courseCode, course.dayAvail, course.semesterAvail, course.startTime, course.endTime))
            conn.commit()
            
        schedule_url = f"http://coursepilot.gcc.edu:3000/Schedule?email={uid}&ScheduleName={schedule_name}"

        return redirect(schedule_url)

#NOTE: NEEDS COMMENTS
@app.route("/api/getAllMajorsAndMinors", methods=["GET"])
def getAllMajorsAndMinors():
    user_email = request.args.get("email")
    global user_dict
    for entry in user_dict: 
        if user_dict[entry] == user_email:
            user_email = entry
    all = MinorRecommendation.getEverythingJSON(user_email)
    return json.dumps(all)


"""
***DATABASE QUERIES FOR DEGREE REPORT***
"""
# Gets all majors of the student signed in from the database
def getStudentMajors(email):
    cursor = conn.cursor()

    studentDegreeQuery = '''select degreeId from StudentMajorMinor join MajorMinor 
                            using(degreeId) where email = %s and isMinor = 0'''

    studentDegrees = []
    try:
        cursor.execute(studentDegreeQuery, (email,))
        studentDegrees = cursor.fetchall()

    except Error as error:
        print("Unable to obtain student majors..." + str(error))

    cursor.close()

    return studentDegrees

# Grabs requirement details from the database pertaining to the specified major
# Includes: degree information; requirement category, details, and hours; and course information
def getMajorRequirements(degreeId):
    cursor = conn.cursor()

    majorReqQuery = '''select degreeName, degreeHrs, reqYear, category from MajorMinor 
                    join MajorMinorRequirements using(degreeId) where degreeId = %s'''

    reqDetailsQuery = '''select category, reqDetails, requiredHrs, totalHrs from Requirement
                        where category = %s and requirementYear = %s'''

    reqCoursesQuery = '''select reqGroup, courseCode, courseName from Requirement join ReqCourses
                        on Requirement.category = ReqCourses.category and requirementYear = catYear
                        join Course using(courseCode) where Requirement.category = %s and 
                        requirementYear = %s'''

    degreeReqDict = {}

    try:
        # Gets degree requirement details
        cursor.execute(majorReqQuery, (degreeId,))
        degreeReq = cursor.fetchall()

        reqCats = []

        # Gets each requirement for the specified degree
        for category in degreeReq:
            reqCats.append(category[3])
        
        studentReqDetails = []

        # Gets information for each requirement under the specified degree
        for req in reqCats:
            # Gets courses related to the requirement specified
            # Note: degreeReq[0][2] is the requirement year
            cursor.execute(reqCoursesQuery, (req, degreeReq[0][2],))

            courses = cursor.fetchall()

            courseList = []

            # Creates a list of courses where each course is a dictionary
            for course in courses:
                courseDict = {
                    #NOTE: MAY NOT NEED REQ_GROUP
                    "req_group": course[0],
                    "course_code": course[1],
                    "course_name": course[2]
                }
                courseList.append(courseDict)

            # Gets details related to the requirement (excluding the courses)
            # Note: degreeReq[0][2] is the requirement year
            cursor.execute(reqDetailsQuery, (req, degreeReq[0][2],))

            reqDetails = cursor.fetchall()

            # Adds the requirement and its details (including the courses) to a list of the degree requirements
            # Note: the requirement information is stored as a dictionary
            for detail in reqDetails:
                reqDict = {
                    "req_category": detail[0],
                    "req_details": detail[1],
                    #NOTE: MAY NOT NEED BOTH REQUIRED HRS AND TOTAL HRS
                    "required_hrs": detail[2],
                    "total_hrs": detail[3],
                    "req_courses": courseList
                }
                studentReqDetails.append(reqDict)
        
        # Final dictionary that has degree information stored as a dictionary
        degreeReqDict = {
            "degree_name": degreeReq[0][0],
            "degree_hours": degreeReq[0][1],
            "req_yr": degreeReq[0][2],
            "req_details": studentReqDetails
        }

    except Error as error:
        print("Unable to obtain student major details..." + str(error))

    cursor.close()

    return degreeReqDict

# Gets all courses from the database
def getAllCourses():
    cursor = conn.cursor()

    selectQuery = "select courseCode, courseName from Course"

    courses = []

    try:
        cursor.execute(selectQuery)

        dbCourses = cursor.fetchall()

        for course in dbCourses:
            courseDict = {
                "course_code": course[0],
                "course_name": course[1],
            }
            courses.append(courseDict)

    except Error as error:
        print("Unable to get courses..." + str(error))
    
    cursor.close()

    return courses

# Gets information for courses the student has taken
def getStudentCourses(email):
    cursor = conn.cursor()

    selectQuery = '''select courseCode, courseName, reqCategory, reqYear from StudentCourses
                    join Course using(courseCode) where email = %s'''

    studentCourses = []

    try:
        cursor.execute(selectQuery, (email,))

        courseDetails = cursor.fetchall()

        # Adds each course as a dictionary to a list of courses
        for course in courseDetails:
            courseDict = {
                "course_code": course[0],
                "course_name": course[1],
                "req_category": course[2],
                "req_yr": course[3]
            }
            studentCourses.append(courseDict)

    except Error as error:
        print("Unable to obtain student courses..." + str(error))
    
    cursor.close()
    
    return studentCourses

# Splits the courses into two groups: ones that were checked and ones that were selected
def parseStudentCourses(email, requirementDetails):
    checkedCourses = []
    selectedCourses = []

    # Get courses from database that the student has completed
    studentCourses = getStudentCourses(email)

    for requirement in requirementDetails["req_details"]:
        # If requirement has courses related to it, it is a checked requirement
        if requirement["req_courses"]:
            for course in studentCourses:
                if course["req_category"] == requirement["req_category"]:
                    checkedCourses.append({"course_code": course["course_code"], "course_name": course["course_name"], "req_category": course["req_category"], "req_yr": course["req_yr"]})
        # If requirement does not have courses related to it, it is a selected requirement
        else:
            for course in studentCourses:
                if course["req_category"] == requirement["req_category"]:
                    selectedCourses.append({"course_code": course["course_code"], "course_name": course["course_name"], "req_category": course["req_category"], "req_yr": course["req_yr"]})
                        
    return {"checked": checkedCourses, "selected": selectedCourses}

# Inserts completed courses into the database
def insertStudentCourses(email, courses):
    cursor = conn.cursor()

    courseQuery = "Insert into StudentCourses(email, courseCode, reqCategory, reqYear) values (%s, %s, %s, %s)"

    studentCourses = getStudentCourses(email)

    try:
        for course in courses:
            # Checks that course is not already in the database
            if not any(c["course_code"] == course["course_code"] and c["req_category"] == course["req_category"] for c in studentCourses):
                cursor.execute(courseQuery, (email, course["course_code"], course["req_category"], course["req_yr"],))
            
        conn.commit()
    
    except Error as error:
        print("Unable to insert courses..." + str(error))
    
    cursor.close()

# Deletes courses that were previously completed but are now incompleted from the database
def deleteStudentCourses(email, courses):
    cursor = conn.cursor()

    deleteQuery = "Delete from StudentCourses where email = %s and courseCode = %s and reqCategory = %s"

    studentCourses = getStudentCourses(email)

    try:
        for course in courses:
            # Checks that course exists in the database
            if any(c["course_code"] == course["course_code"] and c["req_category"] == course["req_category"] for c in studentCourses):
                cursor.execute(deleteQuery, (email, course["course_code"], course["req_category"],))
            
        conn.commit()
    
    except Error as error:
        print("Unable to delete course..." + str(error))

    cursor.close()



#----------------------------------------------------------------------------------------
#                            AUTO GENERATE SCHEDULE ALGORITHM
#
# This algorithm will return a tailored schedule to the user based on the courses they
# have already taken and the ones they can take. The algoritm is weighted heavily on
# prerequisite depth, available times and the courses not taken by the user. 
#
# it runs in three seperate operations
# REMOVAL - remove all the courses the user has taken and the ones they cannot take
# SORT - sort the courses based on their weights
# APPEND - place the courses into a list that will be returned to the user as a schedule
#----------------------------------------------------------------------------------------



# class structure for a student
class Student:
    def __init__(self, name, studentID, studentMajor):
        self.name = name
        self.studentID = studentID
        self.studentMajor = studentMajor

# class structure for a Course (which is different from a class - explained below)
class Course:
    def __init__(self, courseCode, semesterAvail, courseName, creditHours, prerequisites, prerequisiteDepth, courseSection, dayAvail, startTime, endTime):
        self.courseCode = courseCode
        self.semesterAvail = semesterAvail
        self.courseName = courseName
        self.creditHours = creditHours
        self.prerequisites = prerequisites
        self.prerequisiteDepth = prerequisiteDepth
        self.courseSection = courseSection
        self.dayAvail = dayAvail
        self.startTime = startTime
        self.endTime = endTime

'''
class structure for a Class
    Course and Class are different becuase a Course is unique... there is only one Course
    with a Class however there are multiple different sections, times, days avaiable for that
    Course. Thus the Class structure is here to keep account for that
'''
class Class:
    def __init__(self, courseCode=None, semesterAvail=None, timeAvail=None, dayAvail=None, courseSection=None, startTime=None, endTime=None):
        self.courseCode = courseCode
        self.semesterAvail = semesterAvail
        self.timeAvail = timeAvail
        self.dayAvail = dayAvail
        self.courseSection = courseSection
        self.startTime = startTime
        self.endTime = endTime
    

'''
----------------------------------------------------
                    AUTO GENERATION
----------------------------------------------------
This method is the actual algorithm in play. It will
make calls to other functions and use lists generated
by those functions but this is where the logic takes
place for the algorithm to function properly.

user_email - the email of the user
semester_selection - which semester to generate 
                     courses for
----------------------------------------------------
'''
def GetAutoGeneratedSchedule(user_email, semester_selection):
    # list of all the courses the user has already taken
    CoursesTaken = getTakenCourses(user_email)
    # list of all the courses that are required to be taken
    CoursesRequired = getRequiredCourses(user_email)
    # list of all the class times of the required courses
    ClassTimes = getRequiredClasses(CoursesRequired, semester_selection)

    # variable used to determine the year of the user
    creditHoursTaken = getCreditHours(CoursesTaken)
    
    
    for course in CoursesRequired:
        # complicated function to get the prerequisite depth of each course - see below for more detail
        getPrereqDepth(course, course.prerequisiteDepth)

    
    #------------------------------------------
    #                  REMOVAL
    #------------------------------------------

    for courseRequired in CoursesRequired[:]:
        # making sure the course required is in the right semester
        if (courseRequired.semesterAvail != semester_selection and courseRequired.semesterAvail != "both"):
            CoursesRequired.remove(courseRequired)
        # if the user has not taken any courses then any course with prereqs will be removed
        elif (len(CoursesTaken) == 0):
            if (len(courseRequired.prerequisites) != 0):
                CoursesRequired.remove(courseRequired)
        else:
            # variable used to determine if a course should be removed
            removeCourse = False
            for courseTaken in CoursesTaken:
                # if the course has already been taken remove it
                if (courseRequired.courseCode == courseTaken.courseCode):
                    removeCourse = True

            for prereq in courseRequired.prerequisites:
                # prereq size is used as a variable to check if all the prereqs have been taken
                prereqSize = 0
                for courseTaken in CoursesTaken:
                    # if the user has taken the prereq then increment the size
                    if (prereq.courseCode == courseTaken.courseCode):
                        prereqSize += 1
                # if the user hasn't taken the prereqs then remove the course
                if (prereqSize != len(courseRequired.prerequisites)):
                    removeCourse = True

            if (removeCourse == True):
                CoursesRequired.remove(courseRequired)

    # used for displaying the courses in the UI. Making the semester both assures it works with either semester
    for course in CoursesRequired:
        if (course.semesterAvail == "both"):
            course.semesterAvail = semester_selection

    #------------------------------------------
    #                   SORT
    #------------------------------------------
    # sort the courses by their prerequisites in decreasing order
    CoursesRequired.sort(reverse=True, key=sortValue)

    # the schedule that will be returned
    recommendedSchedule = []
    # list used to assure no class overlap
    takenTimes = []

    # used to make sure the user doesn't go over 17 credit hours and get overcharged
    creditHours = 0

    for course in CoursesRequired:
        # if there are no courses currently recommended
        if (len(recommendedSchedule) == 0):
            # checking to make sure the courses time isn't already taken (even though it is the first class)
            if (checkIfTimeAvail(course, ClassTimes, takenTimes) != False):
                # append the course
                recommendedSchedule.append(course)
                creditHours += course.creditHours
        else:
            # making sure there are no two duplicates
            # this should be handled with the Class times but this backs it up to assure no two courses are the same at all
            courseDuplicate = True
            # only one huma should be taken at a time
            oneHuma = True
            # this variable is used to see if the user can take level 300 and 400 courses
            canTakeHigher = True
            for recommendedCourse in recommendedSchedule[:]:
                # checking for a duplicate
                if (recommendedCourse.courseCode == course.courseCode):
                    courseDuplicate = False
                # assuring only one huma
                if (course.courseName[0:3] == "CIV" and recommendedCourse.courseName[0:3] == "CIV" or course.courseCode[0:4] == "HUMA" and recommendedCourse.courseCode[0:4] == "HUMA"):
                    oneHuma = False
                courseLevel = re.findall('\d+', course.courseCode)
                # assuring freshman and sophomores only take 100-200 level courses and seniors can take 300-400 courses
                if (courseLevel[0][:1] == '3' and creditHoursTaken < 30 or courseLevel[0][:1] == '4' and creditHoursTaken < 30):
                    canTakeHigher = False
            # if every check passes
            if (creditHours <= 12 and courseDuplicate == True and oneHuma == True and canTakeHigher == True):
                # if the time is available
                if (checkIfTimeAvail(course, ClassTimes, takenTimes) != False):
                    # add the course
                    recommendedSchedule.append(course)
                    creditHours += course.creditHours
            # reseting the variables
            courseDuplicate = True
            oneHuma = True
            canTakeHigher = True

    return recommendedSchedule
    
'''
----------------------------------------------
This function will return the number of credit
hours the user has taken
----------------------------------------------
CoursesTaken - the courses the user has taken
----------------------------------------------
'''
def getCreditHours(CoursesTaken):
    creditHoursTaken = 0
    for course in CoursesTaken:
        creditHoursTaken += course.creditHours
    return creditHoursTaken

'''
----------------------------------------------
This function checks if a course can be added
without overlap between courses
----------------------------------------------
course - the course in question to be added
ClassTimes - the classtimes of all the courses
takenTimes - the times of all the courses 
            already in the schedule
----------------------------------------------
'''
def checkIfTimeAvail(course, ClassTimes, takenTimes):
    for classTime in ClassTimes:
        # go to the course in question and get it's class times
        if (course.courseCode == classTime.courseCode):
            # if the user already has courses in the recommended schedule
            if (len(takenTimes) != 0):
                # variable to make sure the time is avaiable
                timeFree = True
                for takenTime in takenTimes[:]:
                    # if the timeavail is the same then don't add
                    if (classTime.timeAvail == takenTime.timeAvail):
                        timeFree = False
                    # if the starttime is between the taken time then don't add
                    elif (takenTime.startTime <= classTime.startTime and classTime.startTime <= takenTime.endTime):
                        timeFree = False
                    # if the endtime is between the taken time then don't add
                    elif (takenTime.startTime <= classTime.endTime and classTime.endTime <= takenTime.endTime):
                        timeFree = False
                # if ya can add the course
                if (timeFree == True):
                    # THEN ADD THE COURSE!
                    course.courseSection = classTime.courseSection
                    course.dayAvail = classTime.dayAvail
                    course.startTime = classTime.startTime
                    course.endTime = classTime.endTime
                    takenTimes.append(classTime)
                    return True
            else:
                # if it's the first course to be added then add it
                course.courseSection = classTime.courseSection
                course.dayAvail = classTime.dayAvail
                course.startTime = classTime.startTime
                course.endTime = classTime.endTime
                takenTimes.append(classTime)
                return True
    return False

'''
----------------------------
Used for sorting in reverse
----------------------------
'''
def sortValue(course):
    return course.prerequisiteDepth

'''
---------------------------------------------------
This function is a recursive function that will
return the prerequisite depth of each course.
Prereq depth is given by how many courses need
the course in question... I.E. COMP 141 is needed
by almost every computer science class, thus it
will have a massive prerequisite depth
---------------------------------------------------
course - the course to get prereq depth of
coursePrereqDepth - the current depth of the course
---------------------------------------------------
'''
def getPrereqDepth(course, coursePrereqDepth):
    # base case for the courses that have zero prereqs
    if (len(course.prerequisites) == 0):
        # the default coursePrereqDepth will be 0
        course.prerequisiteDepth = coursePrereqDepth
        return 0
    else:
        for prereq in course.prerequisites:
            # some courses have themselves as a prereq... 
            # this makes sure that wont result in an infinite loop
            if prereq.courseCode != course.courseCode:
                # set this courses prereq depth
                prereq.coursePrereqDepth = coursePrereqDepth
                # RECURSIVE FUNCTION!!!!
                getPrereqDepth(prereq, coursePrereqDepth + 1)
    return 0

'''
---------------------------------------------------
This function will get the courses the user has
already taken and assign them to a class structure
---------------------------------------------------
user_email - the users email
---------------------------------------------------
'''
def getTakenCourses(user_email):

    try:
        # getting all of the courses the user has taken
        cursor = conn.cursor()
        coursesTakenQuery = '''
            select Course.courseCode, Course.courseSemester, Course.courseName, Course.creditHours from StudentCourses JOIN Course 
            on StudentCourses.courseCode = Course.courseCode WHERE StudentCourses.email = %s
        '''
        cursor.execute(coursesTakenQuery, (user_email,))
        info = cursor.fetchall()
        takenCourses = []

        for val in info:
            # creating a new course structure for each course recieved through the query
            newCourse = Course(val[0], val[1], val[2], val[3], [], 0, "", "", "", "")
            takenCourses.append(newCourse)

        return takenCourses
    except error as error:
        print("Could not pull the data" + str(error))

'''
---------------------------------------------------
This function will get the courses the user needs 
to take and assign them to a class structure
---------------------------------------------------
user_email - the users email
---------------------------------------------------
'''
def getRequiredCourses(user_email):
    
    try:
        # getting all of the required courses for the user's major
        cursor = conn.cursor()
        degreeQuery = "select degreeId from StudentMajorMinor WHERE email = %s"
        cursor.execute(degreeQuery, (user_email,))

        # we only want the first value from this query which is the degree ID
        degreeID = cursor.fetchall()[0]
        

        # getting the required courses for the user's major
        requiredCoursesQuery = '''
            select Course.courseCode, Course.courseSemester, Course.courseName, Course.creditHours from Course JOIN ReqCourses ON Course.courseCode = ReqCourses.courseCode 
            JOIN MajorMinorRequirements ON ReqCourses.category = MajorMinorRequirements.category JOIN MajorMinor ON MajorMinorRequirements.degreeId = MajorMinor.degreeId 
            WHERE MajorMinor.degreeId = %s
        '''
        cursor.execute(requiredCoursesQuery, (degreeID))
        info = cursor.fetchall()
        requiredCourses = []

        for val in info:
            # if it is not the first course being created
            if (len(requiredCourses) != 0):
                # variable used to see if we should add a course
                addCourse = True
                # for loop to make sure duplicates don't occur
                for course in requiredCourses:
                    if (course.courseCode == val[0]):
                        addCourse = False
                if (addCourse == True):
                    # add the course!
                    newCourse = Course(val[0], val[1], val[2], val[3], [], 0, "x", "x", "", "")
                    requiredCourses.append(newCourse)
            # if it is the first course being created
            else:
                # add the course!
                newCourse = Course(val[0], val[1], val[2], val[3], [], 0, "x", "x", "", "")
                requiredCourses.append(newCourse)

        # get the prereqs for each of the courses
        prereqQuery = "SELECT * FROM Prerequisite WHERE prereqGroup = 1"
        cursor.execute(prereqQuery)
        prereqs = cursor.fetchall()
        
        # add the prereqs to each course
        for prereq in prereqs:
            for course in requiredCourses:
                if (course.courseCode == prereq[2]):
                    for secondCourse in requiredCourses:
                        if (secondCourse.courseCode == prereq[1]):
                            course.prerequisites.append(secondCourse)

        return requiredCourses

    except error as error:
        print("Could not pull the data" + str(error))


'''
---------------------------------------------------
This function will get the classes the user needs
to take and assign them to a class structure
---------------------------------------------------
user_email - the users email
---------------------------------------------------
'''
def getRequiredClasses(CoursesRequired, semester_selection):
    try:
        # get all of the times for each course
        cursor = conn.cursor()
        semesterQuery = "select * FROM Class WHERE classSemester = %s"
        cursor.execute(semesterQuery, (semester_selection,))
        info = cursor.fetchall()
        times = []

        for val in info:
            # assign them to a class structure
            newClass = Class(val[5], val[1], str(val[2]) + str(val[3]), val[4], val[0], val[2], val[3])
            times.append(newClass)
        

        # only return the times for the courses required
        classTimes = []
        for classTime in times:
            for course in CoursesRequired:
                if (classTime.courseCode == course.courseCode):
                    classTimes.append(classTime)

        return classTimes
    except error as error:
        print("Could not pull the data" + str(error))