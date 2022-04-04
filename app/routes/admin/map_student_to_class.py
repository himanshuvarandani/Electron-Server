import pandas as pd

from app import app
from app.database import db
from app.database import engine
from app.database.models.students import Students
from fastapi import Response
from pydantic import BaseModel

class RequestBody(BaseModel):
    student_id: int
    class_id: int


@app.post("/admin/map-student-to-class")
async def map_student_to_class(
  body: RequestBody, response: Response
):
    try:
        db.query(Students) \
            .filter(Students.id == body.student_id) \
            .update({ 'class_id': body.class_id })
        db.commit()

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
