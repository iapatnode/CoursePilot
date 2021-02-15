import csv
import os, json
from mysql.connector import connect, Error

#Dictionary for inserting entries into the class (not course) table
classDictionary = {}

#Lists to hold the values that will eventually go into the class dictionary
classCode = []
classSection = []
classTitle = []
classCreditHours = []
classDayOfWeek = []
classSemester = []
classStart = []
classEnd = []

#Dictionary for inserting entries into the course table
courseDictionary = {}

courseCode = []
courseName = []
courseHours = []
courseSemester = []

with open('2020-2021.csv', newline='') as f:
    csv_f = csv.reader(f)

    next(csv_f)

    #Parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a string
        day = row[9] + row[10] + row[11] + row[12] + row[13]

        #if the day of the class is not null in the file, 
        # add class specifics to their respective lists
        if day:
            classDayOfWeek.append(day)

            #compiles course code into one string
            code = row[2] + " " + row[3]
            classCode.append(code)

            classSection.append(row[4])

            classTitle.append(row[5])

            classCreditHours.append(row[6])

            #converts time from 12-hour to 24-hour and removes the unnecessary "AM" and "PM"
            if "AM" in row[14]:
                classStart.append(row[14].replace(" AM", ''))
            else:
                oldStart = row[14].replace(" PM", '')

                if oldStart[1] == ":":
                    temp = int(oldStart[0]) + 12
                    classStart.append(oldStart.replace(oldStart[0], str(temp), 1))
                else:
                    classStart.append(oldStart)

            if "AM" in row[15]:
                classEnd.append(row[15].replace(" AM", ''))
            else:
                oldEnd = row[15].replace(" PM", '')

                if oldEnd[1] == ":":
                    tempTwo = int(oldEnd[0]) + 12
                    classEnd.append(oldEnd.replace(oldEnd[0], str(tempTwo), 1))
                else:
                    classEnd.append(oldEnd)

            #checks if class is a fall or spring class
            if row[1] == "10":
                classSemester.append("fall")
            else:
                classSemester.append("spring")

    
    #variables for determining whether the course is offered in the fall, spring, or both
    prevCode = classCode[0]
    semesterLst = []

    #removes duplicate courses since course table only needs one entry of each course
    for index in range(len(classCode)):
        if classCode[index] not in courseCode:
            courseCode.append(classCode[index])
            courseName.append(classTitle[index])
            courseHours.append(classCreditHours[index])

        #determines whether course is offered in fall, spring, or both
        if classCode[index] == prevCode:
            semesterLst.append(classSemester[index])
        else:
            prevCode = classCode[index]

            if "spring" in semesterLst and "fall" in semesterLst:
                courseSemester.append("both")
            elif "spring" in semesterLst:
                courseSemester.append("spring")
            elif "fall" in semesterLst:
                courseSemester.append("fall")

            semesterLst.clear()

            semesterLst.append(classSemester[index])

    #course offering determination for last course in file
    if "spring" in semesterLst and "fall" in semesterLst:
        courseSemester.append("both")
    elif "spring" in semesterLst:
        courseSemester.append("spring")
    elif "fall" in semesterLst:
        courseSemester.append("fall")

# for index in range(len(classCode)):
#     if classCode[index] == "BIOL 234":
#         print(classCode[index])
#         print(classSection[index])
#         print(classSemester[index])
#         print(classDayOfWeek[index])
#         print(classStart[index])
#         print(classEnd[index])
#         print("\n")

#Courses that potentially alternate every semester
alternateCourses = []

with open('2019-2020.csv', newline='') as f:
    csv_f = csv.reader(f)

    next(csv_f)

    #Parse data into their respective columns
    tempClassCode = []
    tempClassSection = []
    tempClassTitle = []
    tempClassCreditHours = []
    tempClassDayOfWeek = []
    tempClassSemester = []
    tempClassStart = []
    tempClassEnd = []

    #Parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a string
        day = row[9] + row[10] + row[11] + row[12] + row[13]

        #if the day of the class is not null in the file, 
        # add class specifics to their respective lists
        if day:
            tempClassDayOfWeek.append(day)

            #compiles course code into one string
            code = row[2] + " " + row[3]
            tempClassCode.append(code)

            tempClassSection.append(row[4])

            tempClassTitle.append(row[5])

            tempClassCreditHours.append(row[6])

            #converts time from 12-hour to 24-hour and removes the unnecessary "AM" and "PM"
            if "AM" in row[14]:
                tempClassStart.append(row[14].replace(" AM", ''))
            else:
                oldStart = row[14].replace(" PM", '')

                if oldStart[1] == ":":
                    temp = int(oldStart[0]) + 12
                    tempClassStart.append(oldStart.replace(oldStart[0], str(temp), 1))
                else:
                    tempClassStart.append(oldStart)

            if "AM" in row[15]:
                tempClassEnd.append(row[15].replace(" AM", ''))
            else:
                oldEnd = row[15].replace(" PM", '')

                if oldEnd[1] == ":":
                    tempTwo = int(oldEnd[0]) + 12
                    tempClassEnd.append(oldEnd.replace(oldEnd[0], str(tempTwo), 1))
                else:
                    tempClassEnd.append(oldEnd)

            #checks if class is a fall or spring class
            if row[1] == "10":
                tempClassSemester.append("fall")
            else:
                tempClassSemester.append("spring")

    #Check to see if the course has not yet been added to our current dictionary, and if so then add its classes to our class dictionary
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in courseCode and tempClassTitle[index] not in courseName:
            classCode.append(tempClassCode[index])
            classSection.append(tempClassSection[index])
            classTitle.append(tempClassTitle[index])
            classCreditHours.append(tempClassCreditHours[index])
            classDayOfWeek.append(tempClassDayOfWeek[index])
            classStart.append(tempClassStart[index])
            classEnd.append(tempClassEnd[index])
            classSemester.append(tempClassSemester[index])

    tempCode = []
    tempCourse = []
    tempHours = []
    tempSemester = []

    #variables for determining whether the course is offered in the fall, spring, or both
    prevCode = tempClassCode[0]
    semesterLst = []

    #removes duplicate courses since course table only needs one entry of each course
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in tempCode:
            tempCode.append(tempClassCode[index])
            tempCourse.append(tempClassTitle[index])
            tempHours.append(tempClassCreditHours[index])

        #determines whether course is offered in fall, spring, or both
        if tempClassCode[index] == prevCode:
            semesterLst.append(tempClassSemester[index])
        else:
            prevCode = tempClassCode[index]

            if "spring" in semesterLst and "fall" in semesterLst:
                tempSemester.append("both")
            elif "spring" in semesterLst:
                tempSemester.append("spring")
            elif "fall" in semesterLst:
                tempSemester.append("fall")

            semesterLst.clear()

            semesterLst.append(tempClassSemester[index])

    #course offering determination for last course in file
    if "spring" in semesterLst and "fall" in semesterLst:
        tempSemester.append("both")
    elif "spring" in semesterLst:
        tempSemester.append("spring")
    elif "fall" in semesterLst:
        tempSemester.append("fall")

    for index in range(len(tempCode)):
        if tempCode[index] not in courseCode and tempCourse[index] not in courseName:
            courseCode.append(tempCode[index])
            courseName.append(tempCourse[index])
            courseSemester.append("alternate")
            courseHours.append(tempHours[index])
        elif tempCode[index] in courseCode:
            courseIndex = courseCode.index(tempCode[index])

            if courseSemester[courseIndex] == "fall" and tempSemester[index] == "spring":
                alternateCourses.append(tempCode[index])
            elif courseSemester[courseIndex] == "spring" and tempSemester[index] == "fall":
                alternateCourses.append(tempCode[index])

    for index in range(len(courseCode)):
        if courseCode[index] not in tempCode and courseName[index] not in tempCourse:
            courseSemester[index] = "alternate"

with open('2018-2019.csv', newline='') as f:
    csv_f = csv.reader(f)

    next(csv_f)

    #Parse data into their respective columns
    tempClassCode = []
    tempClassSection = []
    tempClassTitle = []
    tempClassCreditHours = []
    tempClassDayOfWeek = []
    tempClassSemester = []
    tempClassStart = []
    tempClassEnd = []

    #Parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a string
        day = row[9] + row[10] + row[11] + row[12] + row[13]

        #if the day of the class is not null in the file, 
        # add class specifics to their respective lists
        if day:
            tempClassDayOfWeek.append(day)

            #compiles course code into one string
            code = row[2] + " " + row[3]
            tempClassCode.append(code)

            tempClassSection.append(row[4])

            tempClassTitle.append(row[5])

            tempClassCreditHours.append(row[6])

            #converts time from 12-hour to 24-hour and removes the unnecessary "AM" and "PM"
            if "AM" in row[14]:
                tempClassStart.append(row[14].replace(" AM", ''))
            else:
                oldStart = row[14].replace(" PM", '')

                if oldStart[1] == ":":
                    temp = int(oldStart[0]) + 12
                    tempClassStart.append(oldStart.replace(oldStart[0], str(temp), 1))
                else:
                    tempClassStart.append(oldStart)

            if "AM" in row[15]:
                tempClassEnd.append(row[15].replace(" AM", ''))
            else:
                oldEnd = row[15].replace(" PM", '')

                #TODO: fix this
                if oldEnd[1] == ":":
                    tempTwo = int(oldEnd[0]) + 12
                    tempClassEnd.append(oldEnd.replace(oldEnd[0], str(tempTwo), 1))
                else:
                    tempClassEnd.append(oldEnd)

            #checks if class is a fall or spring class
            if row[1] == "10":
                tempClassSemester.append("fall")
            else:
                tempClassSemester.append("spring")

    #Check to see if the course has not yet been added to our current dictionary, and if so then add its classes to our class dictionary
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in courseCode and tempClassTitle[index] not in courseName:
            classCode.append(tempClassCode[index])
            classSection.append(tempClassSection[index])
            classTitle.append(tempClassTitle[index])
            classCreditHours.append(tempClassCreditHours[index])
            classDayOfWeek.append(tempClassDayOfWeek[index])
            classStart.append(tempClassStart[index])
            classEnd.append(tempClassEnd[index])
            classSemester.append(tempClassSemester[index])

    tempCode = []
    tempCourse = []
    tempHours = []
    tempSemester = []

    #variables for determining whether the course is offered in the fall, spring, or both
    prevCode = tempClassCode[0]
    semesterLst = []

    #removes duplicate courses since course table only needs one entry of each course
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in tempCode:
            tempCode.append(tempClassCode[index])
            tempCourse.append(tempClassTitle[index])
            tempHours.append(tempClassCreditHours[index])

        #determines whether course is offered in fall, spring, or both
        if tempClassCode[index] == prevCode:
            semesterLst.append(tempClassSemester[index])
        else:
            prevCode = tempClassCode[index]

            if "spring" in semesterLst and "fall" in semesterLst:
                tempSemester.append("both")
            elif "spring" in semesterLst:
                tempSemester.append("spring")
            elif "fall" in semesterLst:
                tempSemester.append("fall")

            semesterLst.clear()

            semesterLst.append(tempClassSemester[index])

    #course offering determination for last course in file
    if "spring" in semesterLst and "fall" in semesterLst:
        tempSemester.append("both")
    elif "spring" in semesterLst:
        tempSemester.append("spring")
    elif "fall" in semesterLst:
        tempSemester.append("fall")

    for index in range(len(tempCode)):
        if tempCode[index] not in courseCode and tempCourse[index] not in courseName:
            courseCode.append(tempCode[index])
            courseName.append(tempCourse[index])
            courseSemester.append("alternate")
            courseHours.append(tempHours[index])
        elif tempCode[index] in courseCode:
            courseIndex = courseCode.index(tempCode[index])

            if tempCode[index] in alternateCourses and courseSemester[courseIndex] == "fall" and tempSemester[index] == "fall":
                courseSemester[courseIndex] = "alternate"
            elif tempCode[index] in alternateCourses and courseSemester[courseIndex] == "spring" and tempSemester[index] == "spring":
                courseSemester[courseIndex] = "alternate"

#TODO: Get rest of courses
# for index in range(len(classCode)):
#     if classCode[index] == "BIOL 234":
#         print(classCode[index])
#         print(classSection[index])
#         print(classSemester[index])
#         print(classDayOfWeek[index])
#         print(classStart[index])
#         print(classEnd[index])
#         print("\n")

classDictionary["courseCode"] = classCode
classDictionary["courseSection"] = classSection
classDictionary["classSemester"] = classSemester
classDictionary["meetingDays"] = classDayOfWeek
classDictionary["startTime"] = classStart
classDictionary["endTime"] = classEnd

courseDictionary["courseCode"] = courseCode
courseDictionary["courseName"] = courseName
courseDictionary["courseSemester"] = courseSemester
courseDictionary["creditHours"] = courseHours

if(len(classCode) == len(classSection) and len(classSection) == len(classSemester) and len(classSemester) == len(classDayOfWeek) and len(classDayOfWeek) == len(classStart) and len(classStart) == len(classEnd)):
    print("Class dictionary complete")

if len(courseCode) == len(courseName) and len(courseName) == len(courseSemester) and len(courseSemester) == len(courseHours):
    print("Course dictionary complete")

#Credentials for database connection
scriptdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptdir, "config.json")) as text:
    config = json.load(text)


try:
    #Connects to the Course Pilot database
    conn = connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database=config.get('database'))
    
    cursor = conn.cursor()

    #Inserts Courses into Course table
    # insertCourseQuery = "Insert into Course(courseCode, courseName, creditHours, courseSemester) values (%s, %s, %s, %s)"
    
    # for index in range(len(courseDictionary["courseCode"])):
    #     courseDetails = (courseDictionary["courseCode"][index], courseDictionary["courseName"][index], courseDictionary["creditHours"][index], courseDictionary["courseSemester"][index])
    #     cursor.execute(insertCourseQuery, courseDetails)

    # conn.commit()

    #Inserts classes (course sections) into Class table
    insertClassQuery = "Insert into Class(courseCode, courseSection, classSemester, meetingDays, startTime, endTime) values (%s, %s, %s, %s, %s, %s)"
    
    for index in range(len(classDictionary["courseCode"])):
        classDetails = (classDictionary["courseCode"][index], classDictionary["courseSection"][index], classDictionary["classSemester"][index], classDictionary["meetingDays"][index], classDictionary["startTime"][index], classDictionary["endTime"][index])
        cursor.execute(insertClassQuery, classDetails)

    conn.commit()

    #DB clean up
    cursor.close()
    conn.close()

except Error as error:
    print(error)