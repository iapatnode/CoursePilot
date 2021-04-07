import os
import json
from mysql.connector import connect, Error

# Credentials for database connection
scriptdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptdir, "config.json")) as text:
    config = json.load(text)

# Establishes connection to the database
def connection():
    try:
        conn = connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database=config.get('database'))
        return conn
    except Error as error:
        print(error)

# Gets all majors of the student signed in from the database
def getStudentMajors(email):
    conn = connection()

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
    conn.close()

    return studentDegrees

# Grabs requirement details from the database pertaining to the specified major
# Includes: degree information; requirement category, details, and hours; and course information
def getMajorRequirements(degreeId):
    conn = connection()
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
    conn.close()

    return degreeReqDict

# Gets all courses from the database
def getAllCourses():
    conn = connection()
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
    conn.close()

    return courses

# Gets information for courses the student has taken
def getStudentCourses(email):
    conn = connection()
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
    conn.close()
    
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
# NOTE: NOT FULLY TESTED
def insertStudentCourses(email, courses):
    conn = connection()
    cursor = conn.cursor()

    courseQuery = "Insert into StudentCourses(email. courseCode, reqCategory, reqYear) values (%s, %s, %s, %s)"

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
    conn.close()

# Deletes courses that were previously completed but are now incompleted from the database
# NOTE: NOT FULLY TESTED
def deleteStudentCourses(email, courses):
    conn = connection()
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
    conn.close()
