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

def validLogin(email, password):
    valid = True
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

    return valid

def validPostSignUp(email, password, graduation_year, requirement_year, major, minor):
    cursor = conn.cursor()

    valid = True

    try:
        #gets student's major(s) and minor(s) from MajorMinor table
        studentDegreeQuery = "select degreeID from MajorMinor where degreeName = %s and reqYear = %s and isMinor = %s"

        majorResult = {}
        minorResult = {}

        for ma in major:
            cursor.execute(studentDegreeQuery, (ma, requirement_year, 0))
            majorResult = cursor.fetchall()

        for mi in minor:
            cursor.execute(studentDegreeQuery, (mi, requirement_year, 1))
            minorResult = cursor.fetchall()

        #Adds student to student table
        newStudentQuery = "Insert into Student values (%s, %s, %s)"
        newStudentData = (email, password, graduation_year)

        cursor.execute(newStudentQuery, newStudentData)
        print("Inserted student into the database")

        #Adds student major to respective table
        addToMajorQuery = "Insert into StudentMajorMinor values (%s, %s)"

        for row in majorResult:
            cursor.execute(addToMajorQuery, (email, row[0]))
            print("Inserted one major")

        #Adds student minor to respective table
        addToMinorQuery = "Insert into StudentMajorMinor values (%s, %s)"

        for row in minorResult:
            cursor.execute(addToMinorQuery, (email, row[0]))
            print("Inserted one minor")

        print("Added major/minor to the database")

        conn.commit()

    except Error as error:
        #If you cannot insert the invidual into the database, print error and reroute
        print("Insertion in database unsuccessful: " + str(error))
        valid = False

    cursor.close()
    
    return valid

def validGetSignUp():
        cursor = conn.cursor()
        major_query = "select distinct degreeName from MajorMinor where isMinor = 0"
        minor_query = "select distinct degreeName from MajorMinor where isMinor = 1"

        try:
            cursor.execute(major_query)
            result = cursor.fetchall()
            all_majors = []
            for entry in result:
                all_majors.append(entry[0])
    
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

        except Error as error:
            print("Something went wrong..." + str(error))

            cursor.close()

            return {
                "majors": [],
                "minors": []
            }


