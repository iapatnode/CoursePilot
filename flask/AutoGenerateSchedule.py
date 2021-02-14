# Sam's algorithm


class Student:
    def __init__(self, name, studentID):
        self.name = name
        self.studentID = studentID

class Course:
    def __init__(self, courseCode, prerequisites, timesAvail, semesterAvail, creditHours):
        self.courseCode = courseCode
        self.prerequisites = prerequisites
        self.timesAvail = timesAvail
        self.semesterAvail = semesterAvail
        self.creditHours = creditHours



def AutoGenerateSchedule():
    

    semesterChosen = "fall"

    CoursesTaken = []
    CoursesRequired = []

    

    course1 = Course("COMP 141", [], [], "both", 3)
    course2 = Course("COMP 155", [], [], "fall", 3)
    course3 = Course("COMP 205", ["HUMA 102"], [], "spring", 3)
    course4 = Course("COMP 220", ["COMP 141"], [], "both", 3)
    course5 = Course("COMP 222", [], [], "fall", 3)
    course6 = Course("COMP 233", ["COMP 220"], [], "spring", 3)
    course7 = Course("COMP 244", ["COMP 141"], [], "both", 3)
    course8 = Course("COMP 314", [], [], "spring", 3)
    course9 = Course("COMP 325", [], [], "fall", 3)
    course10 = Course("COMP 340", ["COMP 222", "COMP 325"], [], "both", 3)
    course11 = Course("COMP 342", ["COMP 222"], [], "spring", 3)
    course12 = Course("COMP 350", ["COMP 220"], [], "spring", 3)
    course13 = Course("COMP 401", ["COMP 222"], [], "alternate", 3)
    course14 = Course("COMP 402", ["COMP 222"], [], "alternate", 3)

    
    # removal
    for courseRequired in CoursesRequired:
        for courseTaken in CoursesTaken:
            # if the user has already taken the course then remove it from required courses
            if (courseTaken.courseCode == courseRequired.courseCode):
                CoursesRequired.remove(courseRequired)
            # if the class is in a semester not in the semester chosen remove it from required courses
            elif (courseRequired.semesterAvail != semesterChosen):
                CoursesRequired.remove(courseRequired)

            # need to make sure that all prereqs have been met
            #for coursePrereqs in courseRequired.prerequisites:
            #    if (courseTaken == )
    
    #sorting
    # using insertion sort to sort the array of classes by prereq depth
    for i in range(1, len(CoursesRequired)):
        key = CoursesRequired[i]
        j = i - 1
        while j >= 0 and len(key.prerequisites) < len(CoursesRequired[j].prerequisites):
            CoursesRequired[j + 1] = CoursesRequired[j]
            j -= 1
        courseRequired[j+1] = key

    CourseSchedule = []
    totalHours = 0    
    for courseRequired in CoursesRequired:
        if (totalHours < 17):
            CourseSchedule.append(courseRequired)
    

    return CourseSchedule

'''
REMOVAL

    - run through all the courses not taken
        - if the user has not taken the prereqs then leave this course out
        - if the class is not offered in the semester the user has chosen leave this course out
        - if the class is in a requirement that has already been met

    
SORTING 
    - check for prerequisite depth 
        - Deeper the depth more value on that class
    - Which class has higher need
        - Senior project is worth more than 3D Games
    
    - Smaller but needed things also
        - Make sure user has a science at least once every two semesters
        - Make sure user has a HUMA course at least once every two semesters
        - Make sure user takes SOCIAL science before their 5th semester
        - If the user needs to take SSFT then take before 5th semester

    - Do not need to sort general electives

PRUNE
    Now we are left with a queue of classes with the highest weights first

    - Grab classes out of the queue one by one
        - Check for time conflicts, if the second class conflicts with the first don't use second
        - Assure variety, having at most 3 classes from the same core requirements

'''