import psycopg2 as db
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    @staticmethod
    def connect(query: str, type: str):
        database = db.connect(
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = database.cursor()
        cursor.execute(query)

        if type == "insert":
            database.commit()
            return "Inserted"

        if type == "select":
            return cursor.fetchall()


def show_course_name():
    data = Database.connect("SELECT name FROM courses;", "select")
    course_name = []
    for i in data:
        course_name.append(i[0])
    return course_name