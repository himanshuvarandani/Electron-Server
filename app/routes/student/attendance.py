from app import app
from app.database import db
from app.database.models.attendance import Attendance
from app.database.models.student_subject_map import StudentSubjectMap
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class RequestBody(BaseModel):
    subject_id: int


@app.put("/students/{student_id}/attendance")
async def update_student_attendance(
    student_id, body: RequestBody, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    existing = (
        db.query(StudentSubjectMap)
            .filter(StudentSubjectMap.subject_id == body.subject_id)
            .filter(StudentSubjectMap.student_id == student_id)
            .first()
    )

    if not existing:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "Student not available in given subject"}

    attendance = (
        db.query(Attendance)
            .filter(Attendance.subject_id == body.subject_id)
            .filter(Attendance.student_id == student_id)
            .first()
    )

    try:
        if (attendance):
            attendance.attendance += 1
        else:
            attendance = Attendance()
            attendance.attendance = 1
            attendance.subject_id = body.subject_id
            attendance.student_id = student_id
            
            db.add(attendance)
        db.commit()
    except Exception as e:
        response.status_code = status.HTTP_503_UNAVAILABLE
        return {"result": "fail", "reason": str(e)}

    return {"result": "ok"}


@app.get("/students/{student_id}/attendance")
async def get_student_attendance(
    student_id, subject_id: int, response: Response, Auth: AuthJWT = Depends()
):
    Auth.jwt_required()

    attendance = (
        db.query(Attendance)
            .filter(Attendance.student_id == student_id)
            .filter(Attendance.subject_id == subject_id)
            .first()
    )

    if not attendance:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No attendance found"}

    return attendance
