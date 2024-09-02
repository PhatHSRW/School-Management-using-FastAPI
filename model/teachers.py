from pydantic import BaseModel
from typing import Optional

class TeacherModel(BaseModel):
    name: str
    age: Optional[int] = None
    email: str
    telephone: str