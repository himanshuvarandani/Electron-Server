import pandas as pd

from app import app
from app.database import db
from app.database import engine
from app.database.models.teacher_class_map import TeacherClassMap
from fastapi import Response
from pydantic import BaseModel

class RequestBody(BaseModel):
    teacher_id: int
    class_id: int


@app.post("/admin/teacher-class-map")
async def teacher_class_map(
  body: RequestBody, response: Response
):
    mapping = TeacherClassMap()
    mapping.class_id = body.class_id
    mapping.teacher_id = body.teacher_id

    try:
        db.add(mapping)
        db.commit()

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
