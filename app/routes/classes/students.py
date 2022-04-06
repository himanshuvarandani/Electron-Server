from app import app
from app.database import db
from app.database.models.classes import Classes
from app.database.models.students import Students
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/classes/{class_id}/students")
async def class_students(class_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    students = db.query(Students).filter(Students.class_id == class_id).all()

    if not students:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No students found"}

    return students
