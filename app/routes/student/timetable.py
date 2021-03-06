from app import app
from app.database import db
from app.database.models.student_subject_map import StudentSubjectMap
from app.database.models.timetable import Timetable
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/students/{student_id}/timetable")
async def student_timetable(student_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    timetable = (
        db.query(Timetable)
        .join(StudentSubjectMap, StudentSubjectMap.student_id == student_id)
        .filter(Timetable.subject_id == StudentSubjectMap.subject_id)
        .all()
    )

    if not timetable:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No timetable found"}

    return timetable
