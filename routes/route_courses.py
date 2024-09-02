from fastapi import APIRouter, HTTPException
from model.courses import CourseModel
from model.students import StudentModel
from database.db import courses_collection, teachers_collection, students_collection
from schema.schema import serializeDict, serializeList
from bson import ObjectId

courses_router = APIRouter()

@courses_router.get("/courses")
def find_all_classes():
    return serializeList(courses_collection.find())

@courses_router.post("/courses")
def create_course(course: CourseModel):
    query = {"course_name": course.course_name, "teacher": course.teacher, "teacher_email": course.teacher_email}
    if teachers_collection.find_one({"name": course.teacher, "email": course.teacher_email}) is None:
        return f"This teacher {course.teacher} does not exist in database"
    
    if courses_collection.find_one(query) is None:
        courses_collection.insert_one(dict(course))
        return f"New course {course.course_name} by teacher {course.teacher} was added successfully."
    else:
        return f"This course {course.course_name} by teacher {course.teacher} existed in database."

@courses_router.put("/courses/{id_course}/{id_student}")
def update_student_in_course(id_course, id_student):
    query_course = {"_id": ObjectId(id_course)}
    query_student = {"_id": ObjectId(id_student)}
    if students_collection.find_one(query_student) is None:
        raise HTTPException(status_code=500, detail="No student with this ID in database.")
    if courses_collection.find_one(query_course) is None:
        raise HTTPException(status_code=500, detail="No course with this ID in database.")
    else:
        student = [serializeDict(students_collection.find_one(query_student))["name"],
                        serializeDict(students_collection.find_one(query_student))["email"]]
        course_name = serializeDict(courses_collection.find_one(query_course))["course_name"]
        
        courses_collection.find_one_and_update(query_course, {"$addToSet": {"students":student}})
        courses_collection.update_many(
        {"course_name": {"$ne": course_name}, "students": student},
        {"$pull": {"students": student}}
    )
        students_collection.find_one_and_update(query_student, {"$set": {"class_assigned": course_name}})
    return serializeDict(courses_collection.find_one(query_course))
