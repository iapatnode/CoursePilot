# Nic's Algorithm
"""
1st Pass: Sort the list of minors based on the classes that the student has already taken.
2nd Pass: Sort the list of minors based on the classes that the student has not yet taken but needs to take.
"""



#Dummy Data
class course:
    def __init__(self, code):
        self.code = code

#1st Pass
"""
for each classTaken:
    for each minor:
        if classTaken is in minor.requirements:
            minor.hoursNeeded -= classTaken.hours
"""

#2nd Pass
"""
for each classNotTakenButInMajor:
    for each minor:
        if classNotTakenButInMajor is in minor.requirements:
            minor.hoursNeeded -= classNotTakenButInMajor.hours
"""