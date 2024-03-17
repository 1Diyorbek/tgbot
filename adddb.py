from db import Database

def show_course_name():
    data = Database.connect("SELECT name FROM courses;", "select")
    course_name = []
    for i in data:
        course_name.append(i[0])
    return course_name
