# Nic's Algorithm
"""
1st Pass: Sort the list of minors based on the classes that the student has already taken.
2nd Pass: Sort the list of minors based on the classes that the student has not yet taken but needs to take.
"""

#courseList will be a list of possible courses
#numHoursReequired will contain the number of hours that need to be taken from the courseList
#if it is based on course level, then requiredCourseLevel will != -1 and will be the level necessary
class courseRequirement:
    def __init__(self, courseList, numHoursRequired, hoursRemaining, requiredCourseLevel, classesNotAllowed, requirementMet):
        self.courseList = courseList
        self.numHoursRequired = numHoursRequired
        self.hoursRemaining = hoursRemaining
        self.requiredCourseLevel = requiredCourseLevel
        self.classesNotAllowed = classesNotAllowed
        self.requirementMet = requirementMet
    
    def containsClass(classToCheck):
        if (classToCheck.courseCode in classesNotAllowed):
            return False
        elif (classToCheck.courseCode in courseList):
            if (not requirementMet):
                hoursRemainingInRequirement -= classToCheck.hours
                return True
            else:
                return False
        

#requiredCourses is a list of course requirements
#hoursRemaining is the hours that a given user has remaining
class minor:
    def __init__(self, requiredCourses, hoursRemaining): 
        self.requiredCourses = requiredCourses
        self.hoursRemaining = hoursRemaining

classesTaken = []
remainingClassesInMajor = []
allMinors = []

#1st Pass
"""
for each classTaken:
    for each minor:
        if classTaken is in minor.requirements:
            minor.hoursNeeded -= classTaken.hours
"""
for (classTaken: classesTaken):
    for (minor: allMinors):
        if (minor.requiredCourses.containsClass(classTaken.code)):
            minor.hoursRemaining -= classTaken.hours

#2nd Pass
"""
for each classNotTakenButInMajor:
    for each minor:
        if classNotTakenButInMajor is in minor.requirements:
            minor.hoursNeeded -= classNotTakenButInMajor.hours
"""
for (remainingClass: remainingClassesInMajor):
    for (minor: allMinors):
        if (minor.requiredCourses.containsClass(remainingClass.code)):
            minor.hoursRemaining -= remainingClass.hours

#Database calls -- TO DO: Move this code to better location
#get all minors of a given requirement year
"""
We can begin by just grabbing the minors that are the same requirement year as student's major.
Later, we could add a layer to reccomendations and provide them based on reqYear too.
"""
def getMinors(requirementYear):

"""
Once we obtain the list of minors, we need to get the classes required for each of those minors.
This will most likely be stored in a tree structure or something similar because we need to account for
ands and ors.
"""

"""
JSON?
Minors = ["Mathematics":[1:["MATH101","MATH202"], 2:["MATH365","MATH475"]]]
"""


