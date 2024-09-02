from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')

db =client.school

LIST_COLLECTIONS = ["students", "courses", "teachers"]
for collection_name in LIST_COLLECTIONS:
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

students_collection = db.students
courses_collection = db.courses
teachers_collection = db.teachers

