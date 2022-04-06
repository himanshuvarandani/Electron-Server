from app import app
from app.database import db
from app.database.models.subject_class_map import SubjectClassMap
from app.database.models.subjects import Subjects
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/classes/{class_id}/subjects")
async def class_subjects(class_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    subjects = (
        db.query(Subjects)
        .join(SubjectClassMap, SubjectClassMap.class_id == class_id)
        .filter(Subjects.id == SubjectClassMap.subject_id)
        .all()
    )

    if not subjects:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No subjects found"}

    return subjects
