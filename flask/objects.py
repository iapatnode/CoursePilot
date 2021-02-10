class Class:
    def __init__(self, name, code, semester, hours, section, days):
        self.name = name
        self.code = code
        self.semester = semester
        self.hours = hours
        self.section = section
        self.days = days
    

    def myfunc(self):
        print("Class name is " + self.name + " Code " + self.code + " Semester: " + self.semester + " Hours: " + str(self.hours) + " Days: " + self.days + "Section: " + self.section)





c1 = Class("Intro to Comp Sci", "COMP 101", "fall", 3, 'A', "MWF")
c1.myfunc()