import random
import pandas as pd

from app import app
from app.database import db
from app.database.models.subjects import Subjects
from fastapi import Depends, File, Response
from fastapi_jwt_auth import AuthJWT


@app.post("/admin/add_subjects")
async def add_subjects(
    response: Response, Auth: AuthJWT = Depends(), file: bytes = File(...)
):
    Auth.jwt_required()
    
    try:
        data = pd.read_excel(file, index_col=None)
        subjects = data.values.tolist()

        for subjectDetail in subjects:
            subjectInstance = Subjects()
            subjectInstance.name = subjectDetail[0]

            try:
                db.add(subjectInstance)
                db.commit()
            except Exception as e:
                print(e)

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
