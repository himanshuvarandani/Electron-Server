from app import app
from app.database import db
from app.database.models.teacher_subject_map import TeacherSubjectMap
from app.database.models.timetable import Timetable
from fastapi import Depends, Response, status
from fastapi_jwt_auth import AuthJWT


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
