# Sam's algorithm




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