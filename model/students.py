from pydantic import BaseModel
from typing import Optional

class StudentModel(BaseModel):
    name: str
    age: Optional[int] = None
    email: str
    telephone: Optional[str] = None
    class_assigned: Optional[str] = None
