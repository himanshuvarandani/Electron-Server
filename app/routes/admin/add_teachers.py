import pandas as pd
import uuid

from app import app
from app.database import db
from app.database.models.teachers import Teachers
from fastapi import Depends, File, Response
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash


@app.post("/admin/add_teachers")
async def add_teachers(
    response: Response, Auth: AuthJWT = Depends(), file: bytes = File(...)
):
    Auth.jwt_required()
    
    try:
        dataFrame = pd.read_excel(file, index_col=None)
        teachers = dataFrame.values.tolist()

        passwords = []
        for teacherDetail in teachers:
            teacherInstance = Teachers()
            teacherInstance.name = teacherDetail[0]
            teacherInstance.email = teacherDetail[1]
            teacherInstance.department_name = teacherDetail[2]

            # Generate a random password
            password = uuid.uuid4().hex[:12]
            teacherInstance.password_hash = generate_password_hash(password)
            passwords.append(password)

            try:
                db.add(teacherInstance)
                db.commit()
            except Exception as e:
                print(e)
        
        dataFrame["Password"] = passwords
        teachersFile = pd.ExcelWriter('Teachers.xlsx')
        dataFrame.to_excel(teachersFile)
        teachersFile.save()

        return FileResponse("Teachers.xlsx")
    except Exception as e:
        print(e)
        return {"result": e}
