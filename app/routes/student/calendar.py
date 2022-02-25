from app import app
from app.database import db
from app.database.models.student_subject_map import StudentSubjectMap
from app.database.models.calendar import Calendar
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/students/{student_id}/calendar")
async def student_calendar(student_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    calendar = (
        db.query(Calendar)
        .join(StudentSubjectMap, StudentSubjectMap.student_id == student_id)
        .filter(Calendar.subject_id == StudentSubjectMap.subject_id)
        .all()
    )

    if not calendar:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No calendar found"}

    return calendar
