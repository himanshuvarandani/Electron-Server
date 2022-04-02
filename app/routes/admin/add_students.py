import pandas as pd
import uuid

from app import app
from app.database.models.students import Students
from fastapi import Response, UploadFile, File
from pydantic import BaseModel, validator
from werkzeug.security import generate_password_hash


@app.post("/admin/add_students")
async def add_students(file: bytes = File(...)):
    try:
        data = pd.read_excel(file, index_col=None)
        students = data.values.tolist()

        for studentDetail in students:
            studentInstance = Students()
            studentInstance.name = studentDetail[0]
            studentInstance.email = studentDetail[1]
            studentInstance.class_id = studentDetail[2]

            # Generate a random password
            password = uuid.uuid4().hex[:12]
            studentInstance.password_hash = generate_password_hash(password)

            try:
                db.add(studentInstance)
                db.commit()
            except Exception as e:
                print(e)

        return {"result": "Pass"}
    except Exception as e:
        print(e)
        return {"result": e}
