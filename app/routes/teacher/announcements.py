from app import app
from app.database import db
from app.database.models.announcements import Announcements
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    title: str
    body: str
    teacher_id: int


# Only allow teachers to post announcements
@app.post("/subjects/{subject_id}/announcements")
async def post_subject_announcements(
    subject_id, body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    existing = (
        db.query(TeacherSubjectMap)
        .filter(TeacherSubjectMap.subject_id == subject_id)
        .filter(TeacherSubjectMap.teacher_id == body.teacher_id)
        .first()
    )

    if not existing:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "Teacher not available in given class"}

    announcement = Announcements()
    announcement.title = body.title
    announcement.body = body.body
    announcement.subject_id = subject_id
    announcement.teacher_id = body.teacher_id

    try:
        db.add(announcement)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
