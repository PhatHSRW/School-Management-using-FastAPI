from pydantic import BaseModel
from typing import Optional, List

class CourseModel(BaseModel):
    course_name: str
    teacher: str
    teacher_email: str
    students: List[List[str]] = []

