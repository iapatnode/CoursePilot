# Nic's Algorithm
"""
1st Pass: Sort the list of minors based on the classes that the student has already taken.
2nd Pass: Sort the list of minors based on the classes that the student has not yet taken but needs to take.
"""

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


