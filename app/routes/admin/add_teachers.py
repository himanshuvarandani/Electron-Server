import pandas as pd
import uuid

from app import app
from app.database.models.teachers import Teachers
from fastapi import Response, UploadFile, File
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


@app.post("/admin/add_teachers")
async def add_teachers(file: bytes = File(...)):
    try:
        data = pd.read_excel(file, index_col=None)
        teachers = data.values.tolist()

        for teacherDetail in teachers:
            teacherInstance = Teachers()
            teacherInstance.name = teacherDetail[0]
            teacherInstance.email = teacherDetail[1]

            # Generate a random password
            # Generate a random password
            password = uuid.uuid4().hex[:12]
            teacherInstance.password_hash = generate_password_hash(password)

            try:
                db.add(teacherInstance)
                db.commit()
            except Exception as e:
                print(e)

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
