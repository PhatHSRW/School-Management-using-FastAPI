from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes.route_student import students_router
from routes.route_courses import courses_router
from routes.route_teachers import teachers_router
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(students_router)
app.include_router(courses_router)
app.include_router(teachers_router)

@app.get("/")
def root():
    return "Hello my friend! This is the demo for FastAPI and MongoDB"

@app.get("/index")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

