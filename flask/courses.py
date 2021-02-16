import csv, os, json
from mysql.connector import connect, Error

#lists to hold the values that will eventually go into the Class table
classCode = []
classSection = []
classSemester = []
classStart = []
classEnd = []
classMeetingDays = []

#lists for the sake of filtering course data
classTitle = []
classHours = []

#lists that will eventually go into the Course table
courseCode = []
courseName = []
courseCreditHours = []
courseSemester = []

with open('2020-2021.csv', newline='') as f:
    csv_f = csv.reader(f)

    next(csv_f)

    #parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a single string
        day = row[9] + row[10] + row[11] + row[12] + row[13]

        #if day is not null (i.e., there is a timeslot) then add class to appropriate lists
        if day:
            classMeetingDays.append(day)

            #compiles course code into a single string
            classCode.append(row[2] + " " + row[3])

            classSection.append(row[4])
            classTitle.append(row[5])

            classHours.append(row[6])

            #converts start and end times from 12 hour to 24 hour and removes unnecessary characters
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
        
            #determines class section semester
            if row[1] == "10":
                classSemester.append("fall")
            else:
                classSemester.append("spring")

    #variables for determining whether a course is offered in only fall, only spring, or both
    prevCode = classCode[0]
    semesterList = []

    #removes duplicate courses since course table only needs one entry of each course
    for index in range(len(classCode)):
        if classCode[index] not in courseCode:
            courseCode.append(classCode[index])
            courseName.append(classTitle[index])
            courseCreditHours.append(classHours[index])

        if classCode[index] == prevCode:
            semesterList.append(classSemester[index])
        else:
            if "spring" in semesterList and "fall" in semesterList:
                courseSemester.append("both")
            elif "spring" in semesterList:
                courseSemester.append("spring")
            else:
                courseSemester.append("fall")

            prevCode = classCode[index]

            semesterList.clear()
            semesterList.append(classSemester[index])

    #determines course semester offering for very last course in file
    if "spring" in semesterList and "fall" in semesterList:
        courseSemester.append("both")
    elif "spring" in semesterList:
        courseSemester.append("spring")
    else:
        courseSemester.append("fall")

# print(courseSemester)

#list of courses that potentially alternate every semester
alternateCourses = []

with open('2019-2020.csv', newline='') as f:
    csv_f = csv.reader(f)

    next(csv_f)

    #temporary lists for 2019-2020 class data
    tempClassCode = []
    tempClassSection = []
    tempClassSemester = []
    tempClassTitle = []
    tempClassDays = []
    tempClassHours = []
    tempClassStart = []
    tempClassEnd = []

    #parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a single string
        day = row[9] + row[10] + row[11] + row[12] + row[13]

        #if day is not null (i.e., there is a timeslot) then add class to temporary lists
        if day:
            tempClassDays.append(day)
            tempClassCode.append(row[2] + " " + row[3])
            tempClassTitle.append(row[5])
            tempClassSection.append(row[4])
            tempClassHours.append(row[6])


            #converts start and end times from 12 hour to 24 hour and removes unnecessary characters
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
        
            #determines class section semester
            if row[1] == "10":
                tempClassSemester.append("fall")
            else:
                tempClassSemester.append("spring")

    #temporary lists to hold 2019-2020 course values
    tempCode = []
    tempName = []
    tempHours = []
    tempSemester = []

    #variables for determining whether a course is offered in only fall, only spring, or both
    prevCode = tempClassCode[0]
    semesterList = []

    #removes duplicate courses since course table only needs one entry of each course
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in tempCode:
            tempCode.append(tempClassCode[index])
            tempName.append(tempClassTitle[index])
            tempHours.append(tempClassHours[index])

        if tempClassCode[index] == prevCode:
            semesterList.append(tempClassSemester[index])
        else:
            if "spring" in semesterList and "fall" in semesterList:
                tempSemester.append("both")
            elif "spring" in semesterList:
                tempSemester.append("spring")
            else:
                tempSemester.append("fall")

            prevCode = tempClassCode[index]

            semesterList.clear()
            semesterList.append(tempClassSemester[index])

    #determines course semester offering for very last course in file
    if "spring" in semesterList and "fall" in semesterList:
        tempSemester.append("both")
    elif "spring" in semesterList:
        tempSemester.append("spring")
    else:
        tempSemester.append("fall")

    #adds classes not yet in class list to class list
    for index in range(len(tempClassCode)):
        if tempClassCode[index] not in courseCode:
            classCode.append(tempClassCode[index])
            classSection.append(tempClassSection[index])
            classSemester.append(tempClassSemester[index])
            classStart.append(tempClassStart[index])
            classEnd.append(tempClassEnd[index])
            classMeetingDays.append(tempClassDays[index])

    #adds courses not yet in course list to course list
    for index in range(len(tempCode)):
        if tempCode[index] not in courseCode:
            courseCode.append(tempCode[index])
            courseName.append(tempName[index])
            courseSemester.append("alternate")
            courseCreditHours.append(tempHours[index])
        elif tempCode[index] in courseCode:
            courseIndex = courseCode.index(tempCode[index])

            if courseSemester[courseIndex] == "fall" and tempSemester[index] == "spring":
                alternateCourses.append(tempCode[index])
            elif courseSemester[courseIndex] == "spring" and tempSemester[index] == "fall":
                alternateCourses.append(tempCode[index])
    
    for index in range(len(courseCode)):
        if courseCode[index] not in tempCode:
            courseSemester[index] = "alternate"

with open('2018-2019.csv', newline='') as f:
    csv_f = csv.reader(f)
    
    next(csv_f)

    #temporary lists for 2018-2019 class data
    classCode2018 = []
    classSection2018 = []
    classSemester2018 = []
    classTitle2018 = []
    classDays2018 = []
    classHours2018 = []
    classStart2018 = []
    classEnd2018 = []

    #parses data from each class (row) in the file
    for row in csv_f:
        #converts the list of days the course is offered into a single string
        day = row[16] + row[17] + row[18] + row[19] + row[20]

        #if day is not null (i.e., there is a timeslot) then add class to temporary lists
        if day:
            classDays2018.append(day)
            classCode2018.append(row[3] + " " + row[4])
            classTitle2018.append(row[6])
            classSection2018.append(row[5])
            classHours2018.append(row[7])

            #converts start and end times from 12 hour to 24 hour and removes unnecessary characters
            formattedStart = row[21].replace("1/1/1900 ", '')
            if "AM" in formattedStart:
                classStart2018.append(formattedStart.replace(" AM", ':00'))
            else:
                oldStart = formattedStart.replace(" PM", ':00')

                if oldStart[1] == ":":
                    temp = int(oldStart[0]) + 12
                    classStart2018.append(oldStart.replace(oldStart[0], str(temp), 1) + ":00")
                else:
                    classStart2018.append(oldStart + ":00")

            formattedEnd = row[22].replace("1/1/1900 ", '')
            if "AM" in row[22]:
                classEnd2018.append(formattedStart.replace(" AM", ':00'))
            else:
                oldEnd = formattedEnd.replace(" PM", ':00')

                if oldEnd[1] == ":":
                    tempTwo = int(oldEnd[0]) + 12
                    classEnd2018.append(oldEnd.replace(oldEnd[0], str(tempTwo), 1) + ":00")
                else:
                    classEnd2018.append(oldEnd + ":00")

            if row[1] == "10":
                classSemester2018.append("fall")
            else:
                classSemester2018.append("spring")

    #temporary lists to hold 2018-2019 course values
    tempCode2018 = []
    tempName2018 = []
    tempHours2018 = []
    tempSemester2018 = []

    #variables for determining whether a course is offered in only fall, only spring, or both
    prevCode = classCode2018[0]
    semesterList = []

    #removes duplicate course since course table only needs one entry of each course
    for index in range(len(classCode2018)):
        if classCode2018[index] not in tempCode2018:
            tempCode2018.append(classCode2018[index])
            tempName2018.append(classTitle2018[index])
            tempHours2018.append(classHours2018[index])

        if classCode2018[index] == prevCode:
            semesterList.append(classSemester2018[index])
        else:
            if "spring" in semesterList and "fall" in semesterList:
                tempSemester2018.append("both")
            elif "spring" in semesterList:
                tempSemester2018.append("spring")
            else:
                tempSemester2018.append("fall")

            prevCode = classCode2018[index]

            semesterList.clear()
            semesterList.append(classSemester2018[index])

    if "spring" in semesterList and "fall" in semesterList:
        tempSemester2018.append("both")
    elif "spring" in semesterList:
        tempSemester2018.append("spring")
    else:
        tempSemester2018.append("fall")

    #adds classes not yet in class list to class list
    for index in range(len(classCode2018)):
        if classCode2018[index] not in courseCode:
            classCode.append(classCode2018[index])
            classSection.append(classSection2018[index])
            classSemester.append(classSemester2018[index])
            classStart.append(classStart2018[index])
            classEnd.append(classEnd2018[index])
            classMeetingDays.append(classDays2018[index])

    #adds courses not yet in course list to course list
    for index in range(len(tempCode2018)):
        if tempCode2018[index] not in courseCode:
            courseCode.append(tempCode2018[index])
            courseName.append(tempName2018[index])
            courseSemester.append("alternate")
            courseCreditHours.append(tempHours2018[index])
        else:
            courseIndex = courseCode.index(tempCode2018[index])

            if tempCode2018[index] in alternateCourses and courseSemester[courseIndex] == "fall" and tempSemester2018[index] == "fall":
                courseSemester[courseIndex] = "alternate"
            elif tempCode2018[index] in alternateCourses and courseSemester[courseIndex] == "spring" and tempSemester2018[index] == "spring":
                courseSemester[courseIndex] = "alternate"     

if(len(classCode) == len(classSection) and len(classSection) == len(classSemester) and len(classSemester) == len(classMeetingDays) and len(classMeetingDays) == len(classStart) and len(classStart) == len(classEnd)):
    print("Class lists compiled!")

if(len(courseCode) == len(courseSemester) and len(courseSemester) == len(courseCreditHours) and len(courseCreditHours) == len(courseName)):
    print("Course lists compiled!")

#Credentials for database connection
scriptdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(scriptdir, "config.json")) as text:
    config = json.load(text)

try:
    #Connects to the Course Pilot database
    conn = connect(host=config.get('host'), user=config.get('username'), password=config.get('password'), database=config.get('database'))
    
    cursor = conn.cursor()

    #Inserts Courses into Course table
    insertCourseQuery = "Insert into Course(courseCode, courseName, creditHours, courseSemester) values (%s, %s, %s, %s)"
    
    for index in range(len(courseCode)):
        courseDetails = (courseCode[index], courseName[index], courseCreditHours[index], courseSemester[index])
        cursor.execute(insertCourseQuery, courseDetails)

    conn.commit()

    #Inserts classes (course sections) into Class table
    insertClassQuery = "Insert into Class(courseCode, courseSection, classSemester, meetingDays, startTime, endTime) values (%s, %s, %s, %s, %s, %s)"
    
    for index in range(len(classCode)):
        classDetails = (classCode[index], classSection[index], classSemester[index], classMeetingDays[index], classStart[index], classEnd[index])
        cursor.execute(insertClassQuery, classDetails)

    conn.commit()

    #DB clean up
    cursor.close()
    conn.close()
except Error as error:
    print(error)