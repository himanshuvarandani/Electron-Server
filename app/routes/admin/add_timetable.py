from app import app
from app.database import db
from app.database.models.timetable import Timetable
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    subject_id: int
    meeting_link: str
    start_time: str
    duration: int
    day: str


@app.post("/admin/add_timetable")
async def add_timetable(
    body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()
    
    timetable = Timetable()
    timetable.subject_id = body.subject_id
    timetable.meeting_link = body.meeting_link
    timetable.start_time = body.start_time
    timetable.duration = body.duration
    timetable.day = body.day

    try:
        db.add(timetable)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}
