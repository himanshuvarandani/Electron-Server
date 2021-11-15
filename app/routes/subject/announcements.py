from app import app
from app.database import db
from app.database.models.announcements import Announcements
from app.database.models.subjects import Subjects
from app.database.models.subject_class_map import SubjectClassMap
from app.database.models.teacher_subject_map import TeacherSubjectMap
from fastapi import Response, status
from pydantic import BaseModel


class RequestBody(BaseModel):
    title: str
    body: str
    subject_id: int
    teacher_id: int


@app.get("/subjects/{subject_id}/announcements")
async def get_subject_announcements(subject_id, response: Response):
    announcements = (
        db.query(Announcements)
        .filter(Announcements.subject_id == subject_id)
        .all()
    )

    if not announcements:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No announcements found"}

    return announcements


# Only allow teachers to post announcements
@app.post("/subjects/{subject_id}/announcements")
async def post_subject_announcements(subject_id, body: RequestBody, response: Response):
    existing = (
        db.query(TeacherSubjectMap)
        .filter(TeacherSubjectMap.subject_id == body.subject_id)
        .filter(TeacherSubjectMap.teacher_id == body.teacher_id)
        .first()
    )

    if not existing:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "Teacher not available in given class"}

    announcement = Announcements()
    announcement.title = body.title
    announcement.body = body.body
    announcement.subject_id = body.subject_id
    announcement.teacher_id = body.teacher_id

    try:
        db.add(announcement)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
