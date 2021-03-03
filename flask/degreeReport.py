import os
import json
from mysql.connector import connect, Error


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


def getStudentMajors(email):
    cursor = conn.cursor()

    studentDegreeQuery = "select degreeId from StudentMajorMinor join MajorMinor using(degreeId) where email = %s and isMinor = 0"

    try:
        cursor.execute(studentDegreeQuery, (email,))

        studentDegrees = cursor.fetchall()

        cursor.close()

        return studentDegrees
    except Error as error:
        print("Unable to obtain student majors..." + str(error))
        return []


def getMajorRequirements(degreeId):
    cursor = conn.cursor()

    majorReqQuery = "select degreeName, degreeHrs, reqYear, category from MajorMinor join MajorMinorRequirements using(degreeId) where degreeId = %s"

    reqDetailsQuery = "select category, reqDetails, requiredHrs, totalHrs from Requirement where category = %s and requirementYear = %s"
    
    reqCoursesQuery = "select reqGroup, courseCode, courseName from Requirement join ReqCourses on Requirement.category = ReqCourses.category and requirementYear = catYear join Course using(courseCode) where Requirement.category = %s and requirementYear = %s"
    
    try:
        cursor.execute(majorReqQuery, (degreeId,))

        degreeReq = cursor.fetchall()

        #TODO: CHECK IF DEGREEREQ IS EMPTY

        reqCats = []

        for category in degreeReq:
            reqCats.append(category[3])

        studentReqDetails = []

        for req in reqCats:
            cursor.execute(reqCoursesQuery, (req, degreeReq[0][2],))

            courses = cursor.fetchall()

            courseList = []

            for course in courses:
                courseDict = {
                    "req_group": course[0],
                    "course_code": course[1],
                    "course_name": course[2]
                }
                courseList.append(courseDict)

            cursor.execute(reqDetailsQuery, (req, degreeReq[0][2],))

            reqDetails = cursor.fetchall()

            for detail in reqDetails:
                reqDict = {
                    "req_category": detail[0],
                    "req_details": detail[1],
                    "required_hrs": detail[2],
                    "total_hrs": detail[3],
                    "req_courses": courseList
                }
                studentReqDetails.append(reqDict)

        degreeReqDict = {
            "degree_name": degreeReq[0][0],
            "degree_hours": degreeReq[0][1],
            "req_yr": degreeReq[0][2],
            "req_details": studentReqDetails
        }

        print(degreeReqDict)

        cursor.close()

        return degreeReqDict

    except Error as error:
        print("Unable to obtain student major details..." + str(error))
        return {}