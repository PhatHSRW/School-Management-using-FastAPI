from fastapi import APIRouter, HTTPException, Request
from model.students import StudentModel
from database.db import students_collection
from schema.schema import serializeDict, serializeList
from bson import ObjectId

from fastapi.templating import Jinja2Templates

students_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@students_router.get("/students")
def find_all_students():
    return serializeList(students_collection.find())

@students_router.get("/students/{student_id}")
def find_student(student_id):
    query = {"_id": ObjectId(student_id)}
    if students_collection.find_one(query) is None:
        raise HTTPException(status_code=500, detail="No student with this ID in database.")
    else:
        return serializeDict(students_collection.find_one(query))

@students_router.post("/students")
def create_student(student: StudentModel):
    query = {"name": student.name, "email": student.email}
    if students_collection.find_one(query) is None:
        students_collection.insert_one(dict(student))
        return f"New student {student.name} was added successfully."
    else:
        return f"This student {student.name} existed in database."

@students_router.delete("/students/{student_id}")
def delete_student(student_id):
    query = {"_id": ObjectId(student_id)}
    if students_collection.find_one(query) is None:
        raise HTTPException(status_code=500, detail="No student with this ID in database.")
    else:
        return serializeDict(students_collection.find_one_and_delete(query))

@students_router.put("/students/{student_id}")
def update_student(student_id, student: StudentModel):
    query = {"_id": ObjectId(student_id)}
    if students_collection.find_one(query) is None:
        raise HTTPException(status_code=500, detail="No student with this ID in database.")
    else:
        students_collection.find_one_and_update(query, {"$set": dict(student)})
    return serializeDict(students_collection.find_one(query))


"""USE HTML TEMPLATES"""
# Use templates get_student.html
@students_router.get("/get_student")
async def get_student_form(request: Request):
    return templates.TemplateResponse("get_student.html", {"request": request})

# Use templates get_student.html
@students_router.post("/get_student")
async def get_student(request: Request):
    form_data = await request.form()
    student_email = str.lower(form_data.get("student_email"))

    if "@" not in student_email:
        return templates.TemplateResponse("get_student.html", {"request": request, "error": "Invalid Student Email"})

    student = students_collection.find_one({"email": student_email})
    if student:
        return templates.TemplateResponse("get_student.html", {"request": request, "student_result": student})
    else:
        return templates.TemplateResponse("get_student.html", {"request": request, "error": "Student not found"})
    
@students_router.get("/add_student")
async def get_add_student_form(request: Request):
    return templates.TemplateResponse("add_student.html", {"request": request})

@students_router.post("/add_student")
async def post_add_student(request: Request):
    form_data = await request.form()
    student_data = {
        "name": form_data.get("name"),
        "age": int(form_data.get("age", 0)) if form_data.get("age") else None,
        "email": str.lower(form_data.get("email")),
        "telephone": form_data.get("telephone"),
        "class_assigned": form_data.get("class_assigned")
    }

    query = {"name": student_data["name"], "email": student_data["email"]}
    if students_collection.find_one(query) is None:
        students_collection.insert_one(dict(student_data))
        return templates.TemplateResponse("add_student.html", 
                                          {"request": request, 
                                           "output_message": f"New student was added successfully."})
    else:
        return templates.TemplateResponse("add_student.html", {"request": request, "error": "Student existed in database."})