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
    

    CoursesTaken = []
    CoursesRequired = []

    course1 = Course("ACCT 201", [], [], "fall", 3)
    course2 = Course("ACCT 202", [], [], "spring", 3)
    course3 = Course("ACCT 301", [], [], "fall", 3)
    course4 = Course("")
    course5 =
    course6 =
    course7 =
    course8 =
    course9 =
    course10 =
    course11 =
    course12 =
    course13 =
    course14 =
    course15 =

    CoursesTaken.append()
    


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
        - 

'''