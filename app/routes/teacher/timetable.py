from app import app
from app.database import db
from app.database.models.teacher_subject_map import TeacherSubjectMap
from app.database.models.timetable import Timetable
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    meeting_link: str


@app.put("/timetable/{timetable_id}/update-meeting-link")
async def update_meeting_link(
  timetable_id, body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    try:
        db.query(Timetable) \
            .filter(Timetable.timetable_id == timetable_id) \
            .update({ "meeting_link": body.meeting_link })
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}


@app.get("/teachers/{teacher_id}/timetable")
async def teacher_timetable(teacher_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    timetable = (
        db.query(Timetable)
            .join(TeacherSubjectMap, TeacherSubjectMap.teacher_id == teacher_id)
            .filter(Timetable.subject_id == TeacherSubjectMap.subject_id)
            .all()
    )

    if not timetable:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No timetable found"}

    return timetable
