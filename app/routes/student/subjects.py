from app import app
from app.database import db
from app.database.models.student_subject_map import StudentSubjectMap
from app.database.models.subjects import Subjects
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/students/{student_id}/subjects")
async def student_subjects(student_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    subjects = (
        db.query(Subjects)
        .join(StudentSubjectMap, StudentSubjectMap.student_id == student_id)
        .filter(Subjects.id == StudentSubjectMap.subject_id)
        .all()
    )

    if not subjects:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No subjects found"}

    return subjects
