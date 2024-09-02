from fastapi import APIRouter, HTTPException
from model.teachers import TeacherModel
from database.db import teachers_collection
from schema.schema import serializeDict, serializeList
from bson import ObjectId

teachers_router = APIRouter()

@teachers_router.get("/teachers")
def find_all_teachers():
    return serializeList(teachers_collection.find())

@teachers_router.post("/teachers")
def create_teacher(teacher: TeacherModel):
    query = {"name": teacher.name, "email": teacher.email}
    if teachers_collection.find_one(query) is None:
        teachers_collection.insert_one(dict(teacher))
        return f"New teacher {teacher.name} was added successfully."
    else:
        return f"This teacher {teacher.name} existed in database."

# @teachers_router.delete("/students/{id}")
# def delete_student(id):
#     query = {"_id": ObjectId(id)}
#     if students_collection.find_one(query) is None:
#         raise HTTPException(status_code=500, detail="No student with this ID in database.")
#     else:
#         return serializeDict(students_collection.find_one_and_delete(query))

# @teachers_router.put("/students/{id}")
# def update_student(id, student: StudentModel):
#     query = {"_id": ObjectId(id)}
#     if students_collection.find_one(query) is None:
#         raise HTTPException(status_code=500, detail="No student with this ID in database.")
#     else:
#         students_collection.find_one_and_update(query, {"$set": dict(student)})
#     return serializeDict(students_collection.find_one(query))


