from app import app
from app.database import db
from app.database.models.teacher_subject_map import TeacherSubjectMap
from app.database.models.calendar import Calendar
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


@app.get("/teachers/{teacher_id}/calendar")
async def teacher_timetable(teacher_id, response: Response, Auth: AuthJWT = Depends()):
    Auth.jwt_required()

    calendar = (
        db.query(Calendar)
        .join(TeacherSubjectMap, TeacherSubjectMap.teacher_id == teacher_id)
        .filter(Calendar.subject_id == TeacherSubjectMap.subject_id)
        .all()
    )

    if not calendar:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "fail", "reason": "No calendar found"}

    return calendar
