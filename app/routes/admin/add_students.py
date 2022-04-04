import pandas as pd
import uuid

from app import app
from app.database import db
from app.database.models.students import Students
from fastapi import Depends, File, Response
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash


@app.post("/admin/add_students")
async def add_students(
    response: Response, Auth: AuthJWT = Depends(), file: bytes = File(...)
):
    Auth.jwt_required()
    
    try:
        dataFrame = pd.read_excel(file, index_col=None)
        students = dataFrame.values.tolist()

        passwords = []
        for studentDetail in students:
            studentInstance = Students()
            studentInstance.name = studentDetail[0]
            studentInstance.email = studentDetail[1]

            # Generate a random password
            password = uuid.uuid4().hex[:12]
            studentInstance.password_hash = generate_password_hash(password)
            passwords.append(password)

            try:
                db.add(studentInstance)
                db.commit()
            except Exception as e:
                print(e)
        
        dataFrame["Password"] = passwords
        studentsFile = pd.ExcelWriter('Students.xlsx')
        dataFrame.to_excel(studentsFile)
        studentsFile.save()

        return FileResponse("Students.xlsx")
    except Exception as e:
        print(e)
        return {"result": e}
