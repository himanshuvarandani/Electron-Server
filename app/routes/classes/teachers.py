from app import app
from app.database import db
from app.database.models.teacher_class_map import TeacherClassMap
from app.database.models.teachers import Teachers
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/classes/{class_id}/teachers")
async def class_subjects(class_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    teachers = (
        db.query(Teachers)
        .join(TeacherClassMap, TeacherClassMap.class_id == class_id)
        .filter(Teachers.id == TeacherClassMap.subject_id)
        .all()
    )

    if not teachers:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No teachers found"}

    return teachers
