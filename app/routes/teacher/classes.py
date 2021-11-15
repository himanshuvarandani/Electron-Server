from app import app
from app.database import db
from app.database.models.classes import Classes
from app.database.models.teacher_class_map import TeacherClassMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/teachers/{teacher_id}/classes")
async def teacher_classes(teacher_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    classes = (
        db.query(Classes)
        .join(TeacherClassMap, TeacherClassMap.teacher_id == teacher_id)
        .filter(Classes.id == TeacherClassMap.class_id)
        .all()
    )

    if not classes:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No classes found"}

    return classes
