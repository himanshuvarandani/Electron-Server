import pandas as pd

from app import app
from app.database import db
from app.database import engine
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Response
from pydantic import BaseModel

class RequestBody(BaseModel):
    subject_id: int
    teacher_id: int


@app.post("/admin/teacher-subject-map")
async def teacher_subject_map(
  body: RequestBody, response: Response
):
    mapping = TeacherSubjectMap()
    mapping.teacher_id = body.teacher_id
    mapping.subject_id = body.subject_id

    try:
        db.add(mapping)
        db.commit()

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
