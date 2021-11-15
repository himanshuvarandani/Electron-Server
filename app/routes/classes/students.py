from app import app
from app.database import db
from app.database.models.classes import Classes
from app.database.models.students import Students
from fastapi import Response, status


@app.get("/classes/{class_id}/students")
async def class_students(class_id, response: Response):
    students = db.query(Students).filter(Students.class_id == class_id).all()

    if not students:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No students found"}

    return students
