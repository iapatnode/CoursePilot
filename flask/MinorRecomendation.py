# Nic's Algorithm

from flask import Flask, request, render_template, redirect, session, Response, jsonify
from flask_cors import CORS
import os
import re, json
from mysql.connector import connect, Error
from datetime import datetime
"""
1st Pass: Sort the list of minors based on the classes that the student has already taken.
2nd Pass: Sort the list of minors based on the classes that the student has not yet taken but needs to take.
"""

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

#courseList will be a list of possible courses
#numHoursReequired will contain the number of hours that need to be taken from the courseList
#if it is based on course level, then requiredCourseLevel will != -1 and will be the level necessary
class courseRequirement:
    def __init__(self, courseList, numHoursRequired, totalHours, hoursRemaining, requirementMet):
        self.courseList = courseList
        self.numHoursRequired = numHoursRequired
        self.totalHours = totalHours
        self.hoursRemaining = hoursRemaining
        self.requirementMet = requirementMet
    
    def containsClass(self, classToCheck):
        if (classToCheck.code in self.courseList):
            if (not self.requirementMet):
                self.hoursRemaining -= classToCheck.hours
                return True
            else:
                return False
    def toString(self):
        returnString = "Courses: "
        for course in self.courseList:
            returnString += course
            returnString += ", "
        returnString += "; "
        return returnString
#requiredCourses is a list of course requirements
#hoursRemaining is the hours that a given user has remaining
class major_minor:
    def __init__(self, name, requiredCourses, hoursRemaining, requirementYear): 
        self.name = name
        self.requiredCourses = requiredCourses
        self.hoursRemaining = hoursRemaining
        self.requirementYear = requirementYear
    
    def toString(self):
        returnString = self.name + "... "
        for requiredCourseList in self.requiredCourses:
            returnString += requiredCourseList.toString()
        return returnString

class course:
    def __init__(self, code, hours):
        self.code = code
        self.hours = hours


#Database calls -- TO DO: Move this code to better location
#get all minors of a given requirement year
"""
We can begin by just grabbing the minors that are the same requirement year as student's major.
Later, we could add a layer to reccomendations and provide them based on reqYear too.
"""
def getMinorsByRequirementYear(requirementYear):
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinor WHERE isMinor=1 AND reqYear=%s;''', (requirementYear, ))
    result = cursor.fetchall()
    minors = []
    for entry in result:
        minors.append(major_minor(entry[3], getRequiredClasses(entry[1], requirementYear), entry[4], entry[0]))
    cursor.close()
    return minors


def getMinorsByRequirementYearJSON(requirementYear):
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinor WHERE isMinor=1 AND reqYear=%s;''', (requirementYear, ))
    result = cursor.fetchall()
    minors = []
    for entry in result:
        course_dict = {
            "name": entry[3],
            "requiredClasses": getRequiredClassesJSON(entry[1], requirementYear),
            "hoursRemaining": entry[4],
            "requirementYear": entry[0]
        }
        minors.append(course_dict)
    cursor.close()
    return minors

def getMajorsByRequirementYearJSON(requirementYear):
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinor WHERE isMinor=0 AND reqYear=%s;''', (requirementYear, ))
    result = cursor.fetchall()
    majors = []
    for entry in result:
        course_dict = {
            "name": entry[3],
            "requiredClasses": getRequiredClassesJSON(entry[1], requirementYear),
            "hoursRemaining": entry[4],
            "requirementYear": entry[0]
        }
        majors.append(course_dict)
    cursor.close()
    return majors

def getRequiredClassesJSON(degreeId, reqYear):
    requiredCourses = []
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinorRequirements WHERE degreeId=%s AND catYear=%s;''', (degreeId, reqYear))
    result = cursor.fetchall()
    for entry in result:
        courseList = []
        category = entry[1]
        cursor.execute(''' SELECT * FROM Requirement WHERE category=%s AND requirementYear=%s;''', (category, reqYear))
        categoryResult = cursor.fetchall()
        categoryResult = categoryResult[0]
        categoryName = categoryResult[0]
        numHoursRequired = categoryResult[3]
        totalHours = categoryResult[4]
        hoursRemaining = numHoursRequired
        requirementMet = False
        cursor.execute(''' SELECT * FROM ReqCourses WHERE category=%s AND catYear=%s;''', (category, reqYear))
        courseResult = cursor.fetchall()
        for course in courseResult:
            courseList.append(course[1])
        requiredCourseDict = {
            "name" : categoryName,
            "courseList": courseList,
            "numHoursRequired": numHoursRequired,
            "totalHours": totalHours,
            "hoursRemaining": hoursRemaining,
            "requirementMet": requirementMet
        }
        requiredCourses.append(requiredCourseDict)
    cursor.close()
    return requiredCourses

"""
Once we obtain the list of minors, we need to get the classes required for each of those minors.
This will most likely be stored in a tree structure or something similar because we need to account for
ands and ors.
"""
def getRequiredClasses(degreeId, reqYear):
    validCourseCodes = []
    requiredCourses = []
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinorRequirements WHERE degreeId=%s AND catYear=%s;''', (degreeId, reqYear))
    result = cursor.fetchall()
    for entry in result:
        courseList = []
        category = entry[1]
        cursor.execute(''' SELECT * FROM Requirement WHERE category=%s AND requirementYear=%s;''', (category, reqYear))
        categoryResult = cursor.fetchall()
        categoryResult = categoryResult[0]
        numHoursRequired = categoryResult[3]
        totalHours = categoryResult[4]
        hoursRemaining = numHoursRequired
        requirementMet = False
        cursor.execute(''' SELECT * FROM ReqCourses WHERE category=%s AND catYear=%s;''', (category, reqYear))
        courseResult = cursor.fetchall()
        for course in courseResult:
            courseList.append(course[1])
        requiredCourses.append(courseRequirement(courseList, numHoursRequired, totalHours, hoursRemaining, requirementMet))
    cursor.close()
    return requiredCourses


def getMajorClasses(majorName, reqYear, classesTaken):
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM MajorMinor WHERE degreeName=%s AND reqYear=%s AND isMinor=0;''', (majorName, reqYear))
    result = cursor.fetchall()
    entry = result[0]
    degreeHours = entry[4]
    degreeId = entry[1]
    major = major_minor(majorName, getRequiredClasses(degreeId, reqYear), degreeHours, degreeHours)
    for classTaken in classesTaken:
        for requirement in major.requiredCourses:
            if requirement.containsClass(classTaken):
                    major.hoursRemaining -= classTaken.hours
    cursor.close()

def populateAllMajors(majors, reqYear, classesTaken):
    majorList = []
    for major in majors:
        majorList.append(getMajorClasses(major, reqYear, classesTaken))
    
    return majorList

def getEverythingJSON(user_email):
    majors = getMajorsByRequirementYearJSON(2017)
    majorsTwo = getMajorsByRequirementYearJSON(2018)
    majorsThree = getMajorsByRequirementYearJSON(2019)
    majorsFour = getMajorsByRequirementYearJSON(2020)
    minors = getMinorsByRequirementYearJSON(2017)
    minorsTwo = getMinorsByRequirementYearJSON(2018)
    minorsThree = getMinorsByRequirementYearJSON(2019)
    minorsFour = getMinorsByRequirementYearJSON(2020)
    recMinors = getMinorsByRequirementYearJSON(2017)
    recMinorsTwo = getMinorsByRequirementYearJSON(2018)
    recMinorsThree = getMinorsByRequirementYearJSON(2019)
    recMinorsFour = getMinorsByRequirementYearJSON(2020)

    recommendMinorsJSON(user_email, recMinors)
    recommendMinorsJSON(user_email, recMinorsTwo)
    recommendMinorsJSON(user_email, recMinorsThree)
    recommendMinorsJSON(user_email, recMinorsFour)
    return {"2017" : {"majors" : majors, "minors" : minors, "recMinors" : recMinors}, "2018" : {"majors" : majorsTwo, "minors" : minorsTwo, "recMinors" : recMinorsTwo}, "2019" : {"majors" : majorsThree, "minors" : minorsThree, "recMinors" : recMinorsThree}, "2020" : {"majors" : majorsFour, "minors" : minorsFour, "recMinors" : recMinorsFour}}



def recommendMinors(classesTaken, remainingClassesInMajor, allMinors):
    #1st Pass
    """
    for each classTaken:
        for each minor:
            if classTaken is in minor.requirements:
                minor.hoursNeeded -= classTaken.hours
    """
    for classTaken in classesTaken:
        for minorVar in allMinors:
            for requirement in minorVar.requiredCourses:
                if requirement.containsClass(classTaken):
                    minorVar.hoursRemaining -= classTaken.hours

    #2nd Pass
    """
    for each classNotTakenButInMajor:
        for each minor:
            if classNotTakenButInMajor is in minor.requirements:
                minor.hoursNeeded -= classNotTakenButInMajor.hours
    """
    for remainingClass in remainingClassesInMajor:
        for minorVar in allMinors:
            for requirement in minorVar.requiredCourses:
                if requirement.containsClass(remainingClass):
                    minorVar.hoursRemaining -= remainingClass.hours
    # SORT
    allMinors.sort(key=lambda x: x.hoursRemaining, reverse=False)

def recommendMinorsJSON(userEmail, allMinors):
    classesTaken = getTakenCourses(userEmail)
    remainingClassesInMajor = getRequiredCourses(userEmail)

    classesChecked = []

    #1st Pass
    for classTaken in classesTaken:
        if (classTaken["code"] not in classesChecked):
            classesChecked.append(classTaken["code"])
            
            for minorVar in allMinors:
                usedInMinor = False
                for requirement in minorVar["requiredClasses"]:
                    if usedInMinor == False:
                        if classTaken["code"] in requirement["courseList"]:
                            usedInMinor = True
                            if (requirement["requirementMet"] == False):
                                minorVar["hoursRemaining"] -= classTaken["hours"]
                                requirement["hoursRemaining"] -= classTaken["hours"]
                                if (requirement["hoursRemaining"] <= 0):
                                    requirement["requirementMet"] = True

    #2nd Pass
    for remainingClass in remainingClassesInMajor:
        if remainingClass["code"] not in classesChecked:
            classesChecked.append(remainingClass["code"])
            
            for minorVar in allMinors:
                usedInMinor = False
                for requirement in minorVar["requiredClasses"]:
                    if usedInMinor == False:
                        if remainingClass["code"] in requirement["courseList"]:
                            usedInMinor = True
                            if (requirement["requirementMet"] == False):
                                minorVar["hoursRemaining"] -= remainingClass["hours"]
                                requirement["hoursRemaining"] -= remainingClass["hours"]
                                if (requirement["hoursRemaining"] <= 0):
                                    requirement["requirementMet"] = True
                
    # SORT
    allMinors.sort(key=lambda x: x["hoursRemaining"], reverse=False)

def getTakenCourses(user_email):
    cursor = conn.cursor()
    try:
        cursor.execute("select Course.courseCode, Course.creditHours from StudentCourses JOIN Course on StudentCourses.courseCode = Course.courseCode WHERE StudentCourses.email = %s;", (user_email,))

        info = cursor.fetchall()
        
        takenCourses = []

        for val in info:
            newCourse = {"code": val[0], "hours": val[1]}
            takenCourses.append(newCourse)

        return takenCourses
    except error as error:
        print("Could not pull the data" + str(error))


def getRequiredCourses(user_email):
    
    try:
        cursor = conn.cursor()

        cursor.execute("select degreeId from StudentMajorMinor WHERE email = %s;", (user_email,))

        print(f"User email in minor recommendation: {user_email}")
        degreeID = cursor.fetchall()[0]
        

        #AND Course.courseCode NOT LIKE 'HUMA%' AND Course.courseCode NOT LIKE 'PHYE%' AND Course.courseCode NOT LIKE 'SSFT%' AND Course.courseCode NOT LIKE 'WRIT%'
        cursor.execute("select Course.courseCode, Course.creditHours from Course JOIN ReqCourses ON Course.courseCode = ReqCourses.courseCode JOIN MajorMinorRequirements ON ReqCourses.category = MajorMinorRequirements.category JOIN MajorMinor ON MajorMinorRequirements.degreeId = MajorMinor.degreeId WHERE MajorMinor.degreeId = %s", (degreeID))

        info = cursor.fetchall()


        requiredCourses = []
        for val in info:
            newCourse = {"code": val[0], "hours": val[1]}
            requiredCourses.append(newCourse)

        # add the prereqs to the user
                            
        return requiredCourses

    except error as error:
        print("Could not pull the data" + str(error))
"""
JSON?
Minors = ["Mathematics":[1:["MATH101","MATH202"], 2:["MATH365","MATH475"]]]
"""


'''SELECT degreeName, degreeHrs, Requirement.category, requiredHrs, totalHrs 
FROM MajorMinor JOIN (MajorMinorRequirements JOIN Requirement ON MajorMinorRequirements.category = Requirement.category) ON MajorMinor.degreeId = MajorMinorRequirements.degreeId 
WHERE isMinor=1 AND requirementYear=2017;'''
