from app import app
from app.database import db
from app.database.models.assignments import Assignments
from app.database.models.calendar import Calendar
from app.database.models.attendance import Attendance
from fastapi import Depends, Response
from fastapi_jwt_auth import AuthJWT


# to get all students attendance of a subject for teacher
@app.get("/subjects/{subject_id}/attendances")
async def get_subject_attendances(
    subject_id, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    attendances = db.query(Attendance).filter(Attendance.subject_id == subject_id).all()

    return attendances
