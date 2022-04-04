import pandas as pd

from app import app
from app.database import db
from app.database import engine
from app.database.models.subject_class_map import SubjectClassMap
from fastapi import Response
from pydantic import BaseModel

class RequestBody(BaseModel):
    subject_id: int
    class_id: int


@app.post("/admin/subject-class-map")
async def subject_class_map(
  body: RequestBody, response: Response
):
    mapping = SubjectClassMap()
    mapping.class_id = body.class_id
    mapping.subject_id = body.subject_id

    try:
        db.add(mapping)
        db.commit()

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
