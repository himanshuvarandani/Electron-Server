import pandas as pd

from app import app
from app.database import db
from app.database import engine
from app.database.models.student_subject_map import StudentSubjectMap
from fastapi import Response
from pydantic import BaseModel

class RequestBody(BaseModel):
    subject_id: int
    student_id: int


@app.post("/admin/student-subject-map")
async def student_subject_map(
  body: RequestBody, response: Response
):
    mapping = StudentSubjectMap()
    mapping.student_id = body.student_id
    mapping.subject_id = body.subject_id

    try:
        db.add(mapping)
        db.commit()

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
